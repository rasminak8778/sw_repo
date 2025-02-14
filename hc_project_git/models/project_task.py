# -*- coding: utf-8 -*-
from odoo import fields, models, api
from github import Github
import logging

_logger = logging.getLogger(__name__)

class ProjectTask(models.Model):
    _inherit = 'project.task'

    git_branch_id = fields.Many2one(
        'project.git.branch',
        string='Git Branch',
        help="Select a branch from the chosen GitHub repository.",
    )

    available_git_branches = fields.Many2many(
        'project.git.branch',
        string='Available Git Branches',
        compute='_compute_available_git_branches',
        store=False,
    )
    git_issues_ids= fields.One2many('git.issue',
                                    'task_id', string='Git Issues')

    @api.depends('project_id.github_repo_id')
    def _compute_available_git_branches(self):
        """Fetch branches from the selected GitHub repository dynamically."""
        github_token = self.env['ir.config_parameter'].sudo().get_param(
            'hc_project_git.git_auth_password')

        for task in self:
            if not github_token or not task.project_id.github_repo_id:
                task.available_git_branches = False
                continue

            try:
                g = Github(github_token)
                repo_name = task.project_id.github_repo_id.full_name
                repo = g.get_repo(repo_name)

                branches = []
                for branch in repo.get_branches():
                    existing_branch = self.env['project.git.branch'].search([
                        ('name', '=', branch.name),
                        ('repository_id', '=', task.project_id.github_repo_id.id)
                    ], limit=1)

                    if not existing_branch:
                        existing_branch = self.env['project.git.branch'].create({
                            'name': branch.name,
                            'repository_id': task.project_id.github_repo_id.id,
                        })

                    branches.append(existing_branch.id)

                task.available_git_branches = branches

            except Exception as e:
                _logger.error(f"Error fetching GitHub branches: {str(e)}")
                task.available_git_branches = False

    @api.onchange('available_git_branches')
    def _onchange_available_git_branches(self):
        """Set the first available branch if no branch is selected."""
        if self.available_git_branches and not self.git_branch_id:
            self.git_branch_id = self.available_git_branches[0]

    def action_create_github_issue(self):
        """Opens the issue wizard when button is clicked"""
        self.ensure_one()

        return {
            'name': 'Create Issue Wizard',
            'type': 'ir.actions.act_window',
            'res_model': 'task.issue.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_task_id': self.id,
            }
        }
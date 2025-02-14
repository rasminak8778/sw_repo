# -*- coding: utf-8 -*-
from odoo import fields, models, api
from github import Github
import logging

_logger = logging.getLogger(__name__)

class Project(models.Model):
    _inherit = 'project.project'

    github_repo_id = fields.Many2one(
        'project.git.repo',
        string='GitHub Repo',
        help="Stored GitHub repository selection.",
    )

    available_github_repos = fields.Many2many(
        'project.git.repo',
        string='Available GitHub Repos',
        compute='_compute_available_github_repos',
        store=False,
    )

    @api.depends_context('uid')
    def _compute_available_github_repos(self):
        """Dynamically fetch GitHub repositories when form is opened."""

        github_token = self.env['ir.config_parameter'].sudo().get_param(
            'hc_project_git.git_auth_password')

        for project in self:
            if not github_token:
                _logger.warning("GitHub token not configured.")
                project.available_github_repos = False
                continue

            try:
                git_client = Github(github_token)
                github_user = git_client.get_user()
                repos = []

                for repo in github_user.get_repos():
                    existing_repo = self.env['project.git.repo'].search([
                        ('full_name', '=', repo.full_name)
                    ], limit=1)

                    if not existing_repo:
                        existing_repo = self.env['project.git.repo'].create({
                            'name': repo.name,
                            'full_name': repo.full_name,
                            'repository_url': repo.html_url,
                            'active': True,
                        })

                    repos.append(existing_repo.id)

                project.available_github_repos = repos

            except Exception as e:
                _logger.error(f"Error fetching GitHub repositories: {str(e)}")
                project.available_github_repos = False

    @api.onchange('available_github_repos')
    def _onchange_available_github_repos(self):
        """Save selected repo from dynamically fetched list."""
        if self.available_github_repos:
            self.github_repo_id = self.available_github_repos[0]
# -*- coding: utf-8 -*-
from odoo import fields, models
from github import Github
import logging

_logger = logging.getLogger(__name__)


class ProjectGitRepo(models.Model):
    _name = "project.git.repo"
    _description = "Git Repositories"

    name = fields.Char(string="Repository Name", required=True)
    full_name = fields.Char(string="Full Repository Name", required=True,
                            unique=True)
    repository_url = fields.Char(string="Repository URL")
    active = fields.Boolean(default=True)
    branch_ids = fields.One2many('project.git.branch',
                                 'repository_id', string="Branches")

    def sync_branches(self):
        """Synchronize branches from GitHub."""
        github_token = self.env['ir.config_parameter'].sudo().get_param(
            'hc_project_git.git_auth_password'
        )

        if not github_token:
            _logger.warning("GitHub token not configured.")
            return False

        try:
            github_client = Github(github_token)

            for repo in self:
                github_repo = github_client.get_repo(repo.full_name)
                github_branches = github_repo.get_branches()
                existing_branches = repo.branch_ids.mapped('full_name')

                for branch in github_branches:
                    if branch.name not in existing_branches:
                        self.env['project.git.branch'].create({
                            'name': branch.name,
                            'full_name': branch.name,
                            'repository_id': repo.id,
                            'active': True,
                        })

                current_branches = [b.name for b in github_branches]
                for odoo_branch in repo.branch_ids:
                    odoo_branch.active = odoo_branch.name in current_branches

        except Exception as e:
            _logger.error(f"Error syncing GitHub branches: {str(e)}")
            return False
        return True

    def name_get(self):
        """Custom name display."""
        return [(repo.id, f"{repo.name} ({repo.full_name})") for repo in self]

# -*- coding: utf-8 -*-
from odoo import models, fields
from github import Github
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class TaskIssueWizard(models.TransientModel):
    _name = 'task.issue.wizard'
    _description = 'Task Issue Wizard'

    title = fields.Char('Title', required=True)
    description = fields.Text('Description')
    task_id = fields.Many2one('project.task', string="Task",
                              required=True)

    def action_create_issue(self):
        """Creates GitHub issue when Save button is clicked in wizard"""
        self.ensure_one()

        github_token = self.env['ir.config_parameter'].sudo().get_param(
            'hc_project_git.git_auth_password')

        if not github_token:
            raise ValidationError('GitHub token not configured in settings')
        try:
            github_user = Github(github_token)

            project = self.task_id.project_id
            if not project.github_repo_id:
               raise  ValidationError('No Git repo configured for this project')
            repo = github_user.get_repo(project.github_repo_id.full_name)

            issue = repo.create_issue(
                title=self.title,
                body=self.description if self.description else ""
            )

            self.env['git.issue'].create({
                'title': self.title,
                'description': self.description,
                'task_id': self.task_id.id,
                'project_id': project.id,
                'issue_number': str(issue.number),
                'issue_url': issue.html_url,
                'state': 'open',
            })

            message = f'Ticket has been created successfully.'
            self.task_id.message_post(
                body=message,
            )

            return {
                'type' :'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Success',
                    'message': 'Github Issue created successfully.',
                    'type': 'success',
                    'next': {
                        'type': 'ir.actions.act_window_close'
                    },
                }
            }

        except Exception as e:
            _logger.error(f"Error creating GitHub issue: {str(e)}")
            raise ValidationError(f'Failed to create GitHub issue: {str(e)}')
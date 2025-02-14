# -*- coding: utf-8 -*-
from odoo import fields, models


class GitIssue(models.Model):
    _name = 'git.issue'
    _description = 'Git Issue'
    _rec_name = 'title'

    title = fields.Char('Title', required=True)
    description = fields.Text('Description')
    task_id = fields.Many2one('project.task',
                              string='Related Task')
    project_id = fields.Many2one('project.project',
                                 string='Project')
    issue_number = fields.Char('Issue Number')
    issue_url = fields.Char('Issue URL')
    state = fields.Selection([
        ('open', 'Open'),
        ('closed', 'Closed')
    ], string='State', default='open')
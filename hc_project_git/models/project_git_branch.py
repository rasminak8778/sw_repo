# -*- coding: utf-8 -*-
from odoo import fields, models


class ProjectGitBranch(models.Model):
    _name = 'project.git.branch'
    _description = 'Git Branch'

    name = fields.Char(string="Branch Name", required=True)
    repository_id = fields.Many2one('project.git.repo',
                                    string="Repository", required=True)

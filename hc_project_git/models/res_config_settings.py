# -*- coding: utf-8 -*-
from odoo import models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    git_auth_user = fields.Char(string="Git Username",
                                config_parameter='hc_project_git.git_auth_user')
    git_auth_password = fields.Char(string="Git Password",
                            config_parameter='hc_project_git.git_auth_password')

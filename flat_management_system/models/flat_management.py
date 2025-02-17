# -*- coding: utf-8 -*-
from odoo import fields, models


class FlatManagement(models.Model):
    _name = 'flat.management'
    _description = 'Flat Management'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    user_id = fields.Many2one('res.partner',string='Customer', required= True)
    flat_manage_ids = fields.One2many('flat.flats', 'flat_id', string='Flat details')



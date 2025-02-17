# -*- coding: utf-8 -*-
from odoo import fields, models


class FlatFlats(models.Model):
    _name = 'flat.flats'
    _description = 'Flats'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'

    name = fields.Char('Name', required=True)
    description = fields.Char(string='Description', help='Description for the flat')
    amount = fields.Float(string='Amount')
    flat_id = fields.Many2one('flat.management', string="Flat")

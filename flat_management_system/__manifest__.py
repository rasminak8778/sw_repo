# -*- coding: utf-8 -*-
{
    'name': 'Flat Management',
    'version': '17.0.1.0.0',
    'summary': """This module allows the creation and maangement of Flats""",
    'author': '',
    'website': '',
    'sequence': 0,
    'license': 'GPL-3',
    'description': """  """,
    'category': '',
    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/flat_flats_views.xml',
        'views/flat_management_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': True,
}



# -*- coding: utf-8 -*-
{
    'name': 'Project GitHub',
    'version': '17.0.1.0.0',
    'summary': """This module allows the creation of GitHub issues directly 
                from the Project module.""",
    'author': 'Harrison Consulting',
    'website': 'https://www.harrison.consulting',
    'sequence': 0,
    'license': 'GPL-3',
    'description': """  """,
    'category': 'Project',
    'depends': ['project'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/task_issue_wizard_view.xml',
        'views/project_project_views.xml',
        'views/project_task_views.xml',
        'views/res_config_settings_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': True,
}



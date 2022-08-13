# -*- coding: utf-8 -*-
{
    'name': "employee_relatives",

    'description': "employee relatives management system",

    'author': "ahmed youssef",
    'website': "https://github.com/ay131",

    'sequence': -100,

    'category': 'hr',
    'version': '0.1',
    'application': 'Ture',
    # any module necessary for this one to work correctly
    'depends': ['base', 'hr', 'hr_contract'],

    # always loaded
    'data': [
        'security/security_groups.xml',
        'security/security_rules.xml',
        'security/ir.model.access.csv',

        'data/employee_relatives_sequence.xml',
        'data/state_corn_job.xml',

        'wizar/employee_relatives_report_view.xml',


        'views/hr_employee.xml',
        'views/relatives.xml',
        'views/employee_relatives.xml',
        'views/menu.xml',

        'report/employee_relatives_report_templeate.xml',
        'report/employee_relatives_report_action.xml',

    ],
    # only loaded in demonstration mode
    'demo': [],
}

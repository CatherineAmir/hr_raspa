# -*- coding: utf-8 -*-
{
    'name': 'Hr Raspa',
    'version': '1.0',
    'summary': 'Brief description of the module',
    'description': '''
        Detailed description of the module
    ''',
    'category': 'Uncategorized',
    'author': 'SITA-EGYPT',
    'company': 'SITA-EGYPT',
    'maintainer': 'SITA-EGYPT',
    'website': 'https://sita-eg.com',
    'depends': ['base', 'mail','hr','hr_payroll','report_xlsx'],
    'data': [
        'security/ir.model.access.csv',
        'views/hr_salary_rule.xml',
        'views/payslip_view.xml',
        'reports/payroll_report.xml',
        'wizards/bank_payroll_wizard.xml',
        'views/salary_structure.xml',
        'wizards/batch_wizard_view.xml',
        'views/contract.xml',
    ],
    'license': 'LGPL-3',
    'installable': True,
    'application': False,
    'auto_install': False,
}
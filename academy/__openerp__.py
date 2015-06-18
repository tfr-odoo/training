# -*- coding: utf-8 -*-
{
    'name': "academy",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Your Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Academy',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'product', 'mail', 'board', 'website'],

    # always loaded
    'data': [
        'data.xml',
        'views/course.xml',
        'views/session.xml',
        'views/res_partner.xml',
        'views/res_users.xml',
        'views/billable_product.xml',
        'data/session_workflow.xml',
        'security/groups.xml',
        'security/ir.model.access.csv',
        'security/ir.rule.csv',
        'wizard/export_excel.xml',
        'wizard/subscribe.xml',
        'reports/session.xml',
        'views/dashboard.xml',
        'views/sessionanalysis.xml',
        'views/professor.xml',
        'views/learning.xml',
        'views/proflearn.xml',
        'templates.xml',
        'views/assets_frontend.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo.xml',
    ],
}

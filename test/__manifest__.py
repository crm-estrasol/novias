# -*- coding: utf-8 -*-
{
    'name': "Novias",

    'summary': """
       Funcionalidades extras novias de españa""",

    'description': """
       Modulo afecta y agrega funcionalidades extras a Odoo para el flujo de novias de españa.
    """,

    'author': "Estrasol -Kevin Daniel del Campo",
    'website': "https://estrasol.com.mx/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale','product','mail','web','crm','sale_crm','stock'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/theme/theme.xml',
        'views/crm/crm.xml',
        'views/mail/mail_activity.xml',
        'views/sales/sales.xml',
        'reports/sales_report.xml',
        'reports/reports.xml',
        'wizard/sale_details.xml',
        'mail/mail_taller.xml',
        'views/menus/menus.xml',
    ],  
     'qweb': [
          'qweb/replace_menu_base.xml',
         ]
        ,
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application': True,
}

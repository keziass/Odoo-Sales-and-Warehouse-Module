# -*- coding: utf-8 -*-
{
    'name': "SWALAYAN WAREHOUSE",

    'summary': """
        Swalayan Warehouse Fix AMIN""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/ir_sequence.xml',
        'views/vendor_view.xml',
        'views/cycle_view.xml',
        'views/PO.xml',
        'views/views.xml',
        'views/wh_menu_view.xml',
    ],
}
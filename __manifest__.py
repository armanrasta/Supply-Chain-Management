# -*- coding: utf-8 -*-
{
    'name': "SCM",

    'summary': 'Comprehensive Supply Chain Management Module',

    'description': """
        A robust Supply Chain Management (SCM) module for Odoo,
        encompassing demand forecasting, inventory management, network design,
        procurement, transportation, risk management, performance metrics,
        and technology integration.
    """,

    'author': "Arman Rostami",
    'website': "",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Supply Chain Management',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail', 'stock', 'sale', 'purchase', 'uom', 'account'],
    'application': True,
    'installable': True,
    'auto_install': True,

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/supplier_views.xml',
        'views/supplier_cap_scale_views.xml',
        'views/inventory_views.xml',
        # 'views/views.xml',
        # 'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    # 'test': [
    #     'tests/inventory_inventory_category_test.py',
    #     'tests/inventory_inventory_item_test.py',
    #     'tests/supplier_reliablity_test.py',
    #     'tests/supplier_scalability_plans_test.py',
    #     'tests/supplier_sla_test.py',
    #     'tests/supplier_supplier_test.py',
    # ],
    'license': 'LGPL-3',
}

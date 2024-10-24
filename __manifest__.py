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
        'views/transportation_views.xml',
        'views/demand_forecast_views.xml',
        'views/supplier_relationship_strength_views.xml',
        "views/sla_views.xml",
        "views/contact_person_views.xml",
        
        # 'views/views.xml',
        # 'views/templates.xml',
        
        'data/supplier_supplier_demo.xml',
        'data/inventory_inventory_item_categories_demo.xml',
        'data/inventory_inventory_item_demo.xml',
        'data/inventory_warehouse_location_demo.xml',
        # 'data/supplier_capacity_demo.xml',
        'data/supplier_carbon_objective_demo.xml',
        'data/supplier_contact_person_demo.xml',
        'data/supplier_cost_competitiveness_demo.xml',
        # 'data/supplier_demand_forecast_demo.xml',
        # 'data/supplier_mst_demo.xml',
        # 'data/supplier_network_robustness_demo.xml',
        # 'data/supplier_product_innovation_demo.xml',
        # 'data/supplier_rd_investment_demo.xml',
        # 'data/supplier_relationship_strength_demo.xml',
        # 'data/supplier_reliability_demo.xml',
        # 'data/supplier_scalibility_plans_demo.xml',
        'data/supplier_sla_demo.xml',
        'data/supplier_trade_off_weight_demo.xml',
        'data/supplier_transportation_mode_demo.xml',
        'data/supplier_transportation_plan_demo.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
    
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

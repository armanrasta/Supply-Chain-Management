from odoo import models, fields, api
from odoo.exceptions import ValidationError


class NetworkRobustness(models.Model):
    _name = 'scm.network_robustness'
    _description = 'Network Design Robustness Parameter'

    name = fields.Char(string='Parameter Name', required=True)
    description = fields.Text(string='Description')
    value = fields.Float(string='Value', required=True, help='Value representing the robustness metric.')
    inventory_item_id3 = fields.Many2many(
        'scm.inventory_item',
        'network_robustness_inventory_rel',  # custom relation table
        'network_robustness_id',  # first column name (self side)
        'inventory_item_id3',  # second column name (related model side)
        string='Related Inventory Items'
    )
    transportation_mode_id = fields.Many2many(
        'scm.transportation_mode',
        'network_robustness_transportation_rel',  # custom relation table
        'network_robustness_id',  # first column name (self side)
        'transportation_mode_id',  # second column name (related model side)
        string='Related Transportation Modes'
    )
    active = fields.Boolean(string='Active', default=True)
    supplier_id = fields.Many2many(
        comodel_name='scm.supplier',
        relation='network_robustness_supplier_rel',  # Custom relation table name
        column1='network_robustness_id',            # Column referencing this model
        column2='supplier_id',                       # Column referencing related model
        string='Related Suppliers'
    )
    
    _sql_constraints = [
        ('unique_parameter_name', 'UNIQUE(name)', 'Each robustness parameter must have a unique name.')
    ]

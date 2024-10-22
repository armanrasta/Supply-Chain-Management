from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Supplier(models.Model):
    _name = 'scm.supplier'
    _description = 'Supplier'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Supplier Name', required=True )
    contact_email = fields.Char(string='Contact Email' )
    contact_phone = fields.Char(string='Contact Phone' )
    address = fields.Text(string='Address' )
    active = fields.Boolean(string='Active', default=True)
    performance_score = fields.Float(
        string='Supplier Rating',
        digits=(1, 2),
        compute='_compute_performance_score',
        default=0.0
       )
    
    network_robustness_id = fields.Many2many(
        comodel_name='scm.network_robustness',
        relation='network_robustness_supplier_rel',  # Relation table name
        column1='supplier_id',                       # Column referencing this model
        column2='network_robustness_id',             # Column referencing related model
        string='Network Robustness Parameters'
    )
    demand_forecast_id = fields.One2many(
        comodel_name='scm.demand_forecast',
        inverse_name='supplier_id3',
        string='Demand Forecasts'
    )
    capacity_id = fields.One2many(
        comodel_name='scm.supplier_capacity',
        inverse_name='supplier_id5', 
        string='Production Capacities'
    )
    scalability_id = fields.One2many(
        comodel_name='scm.supplier_scalability', 
        inverse_name='supplier_id6', 
        string='Scalability Plans'
    )
    contact_person_id = fields.One2many(
        comodel_name='scm.supplier_contact_person', 
        inverse_name='supplier_id1', 
        string='Contact Persons'
    )
    reliability_id = fields.One2many(
        comodel_name='scm.supplier_reliability', 
        inverse_name='supplier_id2', 
        string='Reliability Indices'
    )
    supplier_cost_competitiveness_id = fields.One2many(
        comodel_name='scm.supplier_cost_competitiveness', 
        inverse_name='supplier_id10', 
        string='Supplier Cost Competitiveness'
    )
    supplier_relationship_strength_id = fields.One2many(
        comodel_name='scm.supplier_relationship_strength',
        inverse_name='supplier_id9',
        string='Supplier Relationship Strength'
    )
    supplier_rd_investment_id = fields.One2many(
        comodel_name='scm.supplier_rd_investment',
        inverse_name='supplier_id7',
        string='Supplier R/D Investment'
    )
    supplier_product_innovation_id = fields.One2many(
        comodel_name='scm.supplier_product_innovation',
        inverse_name='supplier_id8',
        string='Supplier Product Innovation'
    )
    
    # Corrected Many2many Field for Carbon Objectives
    carbon_objective_id = fields.Many2many(
        comodel_name='scm.carbon_objective',
        relation='supplier_carbon_relation',  # Relation table name (same as in CarbonObjective)
        column1='supplier_id4',                # Current model's reference
        column2='carbon_objective_id',        # Related model's reference
        string='Carbon Objectives'
    )
    
    inventory_item_id = fields.Many2many(
        comodel_name='scm.inventory_item',  
        # relation='inventory_supplier_relation',  # Relation table name
        # column1='supplier_id13',                    # Current model's reference
        # column2='inventory_item_id',              # Related model's reference
        string='Inventory Items',
    )
    
    @api.constrains('performance_score')
    def _check_rating(self):
        for supplier in self:
            if supplier.performance_score < 0 or supplier.performance_score > 5:
                raise ValidationError("Supplier rating must be between 0 and 5.")

    @api.depends('reliability_id.overall_reliability')
    def _compute_performance_score(self):
        for supplier in self:
            if supplier.reliability_id:
                total_reliability = sum(s.overall_reliability for s in supplier.reliability_id)
                supplier.performance_score = total_reliability / len(supplier.reliability_id)
            else:
                supplier.performance_score = 0.0

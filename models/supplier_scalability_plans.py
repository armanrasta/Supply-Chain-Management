from odoo import models, fields


class ScalabilityPlans(models.Model): # Supplier Capacity & Scalability 
    _name = 'scm.supplier_scalability'
    _description = 'Supplier Capacity & Scalability: Scalability Plans'
    
    supplier_id6 = fields.Many2one('scm.supplier', string='Supplier', ondelete='cascade', required=True)
    scale_up_plan = fields.Text(string='Scale-Up Plan', help='Details of how the supplier plans to increase production capacity based on demand.')
    scale_down_plan = fields.Text(string='Scale-Down Plan', help='Details of how the supplier plans to reduce production capacity if demand decreases.')
    investment_required = fields.Float(string='Investment Required', help='The amount of investment needed to implement scalability plans.')
    time_to_scale_up = fields.Integer(string='Time to Scale Up (Days)', help='Number of days required to increase production capacity.')
    time_to_scale_down = fields.Integer(string='Time to Scale Down (Days)', help='Number of days required to decrease production capacity.')
    scale_up_capacity = fields.Float(string='Scale-Up Capacity (%)', help='Expected percentage increase in production capacity when scaling up.')
    scale_down_capacity = fields.Float(string='Scale-Down Capacity (%)', help='Expected percentage decrease in production capacity when scaling down.')

    _sql_constraints = [
        ('unique_supplier_scalability', 'UNIQUE(supplier_id6)', 'Each supplier can have only one scalability plan.')
    ]
    
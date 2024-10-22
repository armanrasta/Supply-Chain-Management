from odoo import models, fields, api
from odoo.exceptions import ValidationError


class SupplierCapacity(models.Model): # Supplier Capacity & Scalability 
    _name = 'scm.supplier_capacity'
    _description = 'Supplier Capacity & Scalability: Supplier Production Capacity'
    
    supplier_id5 = fields.Many2one('scm.supplier', string='Supplier', ondelete='cascade', required=True)
    product_id = fields.Many2one('product.product', string='Product', ondelete='cascade', required=True)
    max_capacity = fields.Float(string='Max Capacity', help='Maximum production capacity per period (e.g., per month).')
    min_capacity = fields.Float(string='Min Capacity', help='Minimum production capacity per period.')
    current_utilization = fields.Float(string='Current Utilization (%)', help='Percentage of the supplier’s capacity that is currently utilized.')
    utilization_trend = fields.Float(string='Utilization Trend (%)', help='Changes in utilization over a certain period, useful for tracking growth or reductions in capacity usage.')
    lead_time = fields.Integer(string='Lead Time (Days)', help='Estimated lead time for production based on current capacity.')
    last_review_date = fields.Date(string='Last Review Date', help='Date when the capacity was last reviewed.')
    capacity_type = fields.Selection([
        ('normal', 'Normal'),
        ('peak', 'Peak'),
        ('off_peak', 'Off-Peak'),
    ], string='Capacity Type', help='Type of capacity based on production periods.')
    capacity_status = fields.Selection([
    ('stable', 'Stable'),
    ('increasing', 'Increasing'),
    ('decreasing', 'Decreasing'),
    ], string='Capacity Status', help='Current status of the supplier’s production capacity.')
    period = fields.Selection([
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('yearly', 'Yearly'),
    ], string='Period', default='monthly', required=True, help='The period for which the capacity is measured.')
    
    _sql_constraints = [
        ('unique_supplier_product_period', 'UNIQUE(supplier_id5, period)', 'Capacity data must be unique per supplier, product, and period.')
    ]

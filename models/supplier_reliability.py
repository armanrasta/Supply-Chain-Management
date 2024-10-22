from odoo import models, fields, api


class SupplierReliability(models.Model):
    _name = 'scm.supplier_reliability'
    _description = 'Supplier Reliability Index'
    _order = 'date DESC'

    supplier_id2 = fields.Many2one('scm.supplier', string='Supplier', ondelete='cascade', required=True)
    date = fields.Date(string='Date', required=True, default=fields.Date.today)
    on_time_delivery = fields.Float(string='On-Time Delivery (%)', help='Percentage of orders delivered on time.')
    quality = fields.Float(string='Quality Score', help='Quality score of delivered goods.')
    responsiveness = fields.Float(string='Responsiveness Score', help='Responsiveness in addressing issues.')
    overall_reliability = fields.Float(string='Overall Reliability', compute='_compute_overall_reliability', store=True, readonly=True)

    @api.depends('on_time_delivery', 'quality', 'responsiveness')
    def _compute_overall_reliability(self):
        for record in self:
            # Simple average; adjust weights as needed
            record.overall_reliability = (record.on_time_delivery + record.quality + record.responsiveness) / 3

    _sql_constraints = [
        ('unique_supplier_date', 'UNIQUE(supplier_id2, date)', 'Reliability metrics for a supplier on a specific date must be unique.')
    ]
    
from odoo import models, fields


class SLA(models.Model): # Customer Service Level Agreements
    _name = 'scm.sla'
    _description = 'Customer Service Level Agreement'

    # customer_id = fields.Many2one('res.partner', string='Customer', ondelete='cascade', required=True) #unique
    name = fields.Char(string='SLA Name', required=True)
    fulfillment_rate = fields.Float(string='Order Fulfillment Rate (%)', help='Target percentage of orders to be fulfilled on time.')
    delivery_time = fields.Integer(string='Delivery Time (Days)', help='Maximum days for order delivery.')
    support_response_time = fields.Integer(string='Support Response Time (Hours)', help='Maximum hours to respond to support inquiries.')
    active = fields.Boolean(string='Active', default=True)

    _sql_constraints = [
        ('unique_customer_sla', 'UNIQUE( name)', 'Each customer can have unique SLA names.')
    ]

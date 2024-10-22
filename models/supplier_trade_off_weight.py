from odoo import models, fields, api


class TradeOffWeight(models.Model):
    _name = 'scm.tradeoff_weight'
    _description = 'Trade-off Weights for Cost and Service Metrics'

    name = fields.Char(string='Weight Name', required=True)
    cost_weight = fields.Float(string='Cost Weight', default=1.0, help='Weight assigned to cost metrics.')
    service_weight = fields.Float(string='Service Weight', default=1.0, help='Weight assigned to service metrics.')
    description = fields.Text(string='Description')
    active = fields.Boolean(string='Active', default=True)

    _sql_constraints = [
        ('unique_weight_name', 'UNIQUE(name)', 'Each trade-off weight configuration must have a unique name.')
    ]

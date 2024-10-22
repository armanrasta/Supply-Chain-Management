from odoo import models, fields


class TransportationPlan(models.Model):
    _name = 'scm.transportation_plan'
    _description = 'Transportation Plan'

    name = fields.Char(string='Plan Name', required=True)
    transportation_mode_id = fields.Many2one(
        'scm.transportation_mode', string='Transportation Mode', required=True)  # check
    tradeoff_weight_id = fields.Many2one(
        'scm.tradeoff_weight', string='Trade-off Weight', required=True)  # check

    _sql_constraints = [
        ('unique_plan_name', 'UNIQUE(name)',
         'Each transportation plan must have a unique name.')
    ]

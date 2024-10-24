from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ModeSpecificTransportationCost(models.Model):
    _name = 'scm.mode_specific_transportation_cost'
    _description = 'Mode-Specific Transportation Cost'
    _order = 'transport_mode_id, date_effective DESC'

    transport_mode_id = fields.Many2one(
        'scm.transportation_mode', string='Transport Mode', required=True, ondelete='cascade')
    carrier_id = fields.Many2one('res.partner', string='Carrier', domain=[
        ('supplier_rank', '>', 0)], required=True, ondelete='restrict')
    date_effective = fields.Date(
        string='Effective Date', required=True, default=fields.Date.today)
    cost_per_km = fields.Float(
        string='Cost per KM', required=True, digits=(10, 2))
    cost_per_hour = fields.Float(
        string='Cost per Hour', required=True, digits=(10, 2))
    fixed_cost = fields.Float(
        string='Fixed Cost', required=True, digits=(10, 2))
    variable_cost_percentage = fields.Float(
        string='Variable Cost (%)', required=True, help='Percentage of variable costs based on total cost.')

    _sql_constraints = [
        ('unique_mode_carrier_date', 'UNIQUE(transport_mode_id, carrier_id, date_effective)',
         'Each carrier can have only one cost entry per transport mode and effective date.'),
        ('positive_costs', 'CHECK(cost_per_km >= 0 AND cost_per_hour >= 0 AND fixed_cost >= 0 AND variable_cost_percentage >= 0)',
         'All costs must be non-negative.'),
    ]

    @api.constrains('variable_cost_percentage')
    def _check_variable_cost_percentage(self):
        for record in self:
            if not (0 <= record.variable_cost_percentage <= 100):
                raise ValidationError(
                    'Variable Cost Percentage must be between 0 and 100.')

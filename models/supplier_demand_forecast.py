from odoo import models, fields, api
from odoo.exceptions import ValidationError


class DemandForecast(models.Model):
    _name = 'scm.demand_forecast'
    _description = 'Multi-Period Demand Forecast'
    _order = 'period_start_date DESC'

    inventory_item_id2 = fields.Many2one('scm.inventory_item', string='Inventory Item', ondelete='cascade', required=True)
    scenario = fields.Selection([
        ('best', 'Best Case'),
        ('worst', 'Worst Case'),
        ('most_likely', 'Most Likely'),
    ], string='Scenario', required=True)
    period_start_date = fields.Date(string='Period Start Date', required=True)
    period_end_date = fields.Date(string='Period End Date', required=True)
    forecasted_quantity = fields.Integer(string='Forecasted Quantity', required=True)
    active = fields.Boolean(string='Active', default=True)
    supplier_id3 = fields.Many2one('scm.supplier', string='Supplier', ondelete='restrict')
    
    _sql_constraints = [
        ('unique_item_scenario_period', 'UNIQUE(inventory_item_id2, scenario, period_start_date, period_end_date)', 'Each forecast must be unique per inventory item, scenario, and period.')
    ]

    @api.constrains('period_start_date', 'period_end_date')
    def _check_period_dates(self):
        for record in self:
            if record.period_end_date < record.period_start_date:
                raise ValidationError('Period end date must be after the start date.')

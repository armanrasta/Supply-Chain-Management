from odoo import models, fields


class Region(models.Model):
    _inherit = 'res.country.state'

    demand_multiplier = fields.Float(
        string='Demand Multiplier', default=1.0, help='Factor to adjust demand forecasts for this region')

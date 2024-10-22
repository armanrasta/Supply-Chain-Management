from odoo import models, fields, api
from odoo.exceptions import ValidationError


# Suppliers' investments in research and development.
class SupplierRDInvestment(models.Model):
    _name = 'scm.supplier_rd_investment'
    _description = 'Supplier R&D Investment Levels'

    supplier_id7 = fields.Many2one(
        'scm.supplier', string='Supplier', ondelete='cascade', required=True)
    amount_invested = fields.Float(
        string='Amount Invested', required=True, help='Total amount invested in R&D.')
    currency_id = fields.Many2one('res.currency', string='Currency', required=True,
                                  default=lambda self: self.env.company.currency_id, help="Currency in which the investment is recorded.")
    investment_period_start = fields.Date(
        string='Investment Period Start', required=True, help='Start date of the R&D investment period.')
    investment_period_end = fields.Date(
        string='Investment Period End', required=True, help='End date of the R&D investment period.')
    investment_trend = fields.Float(
        string='Investment Trend (%)', help='Percentage increase or decrease in R&D investments compared to the previous period.')

    research_focus = fields.Many2one('scm.research_focus', string='Research Focus',
                                     help='The primary area of research the investment is focused on (e.g., materials, technology, sustainability).')
    expected_roi = fields.Float(string='Expected ROI (%)',
                                help='The estimated return on investment for the R&D investment as a percentage.')
    actual_roi = fields.Float(
        string='Actual ROI (%)', help='The actual return on investment after the R&D investment.')
    rd_collaboration = fields.Boolean(string='Collaboration with External Entities',
                                      help='Indicates whether the R&D was done in collaboration with universities, research institutes, or other companies.')
    environmental_impact = fields.Selection([('low', 'Low'), ('medium', 'Medium'), ('high', 'High')],
                                            string='Environmental Impact', help='Estimated environmental impact of the R&D projects.')
    _sql_constraints = [
        ('unique_supplier_investment_period', 'UNIQUE(supplier_id7, investment_period_start, investment_period_end)',
         'R&D investment for a supplier must be unique for a given period.')
    ]

    @api.constrains('investment_period_end', 'investment_period_start')
    def _check_investment_period(self):
        for record in self:
            if record.investment_period_end < record.investment_period_start:
                raise ValidationError(
                    'Investment period end date must be after the start date.')

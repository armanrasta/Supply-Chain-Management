from odoo import models, fields, api
from datetime import timedelta


class SupplierProductInnovation(models.Model):
    _name = 'scm.supplier_product_innovation'
    _description = 'Supplier Product Innovation Rates'

    supplier_id8 = fields.Many2one(
        'scm.supplier', string='Supplier', ondelete='cascade', required=True)
    product_id = fields.Many2one('product.product', string='Product',
                                 required=True, help='New product introduced by the supplier.')
    introduction_date = fields.Date(
        string='Introduction Date', required=True, help='Date when the new product was introduced.')
    product_category_id = fields.Many2one(
        'product.category', string='Product Category', help='Category of the newly introduced product.')
    innovation_rate = fields.Float(string='Innovation Rate', compute='_compute_innovation_rate',
                                   store=True, help='Calculated frequency of new product introductions.')
    description = fields.Text(
        string='Description', help='Details about the new product or innovation.')
    innovation_type = fields.Selection([('incremental', 'Incremental'), ('radical', 'Radical')],
                                       string='Type of Innovation',
                                       help='Defines whether the product introduction is incremental (small improvement) or radical (significant new product or breakthrough).')
    development_time = fields.Float(string='Development Time (months)',
                                    help='Total time taken to develop the product from conception to introduction.')
    market_impact = fields.Selection([('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], string='Market Impact',
                                     help='Estimation of the product’s potential impact on the market.')
    patent_filed = fields.Boolean(string='Patent Filed',
                                  help='Indicates whether a patent has been filed for the new product or technology.')
    sustainability_index = fields.Float(string='Sustainability Index',
                                        help='Measures how sustainable the new product is, based on factors like energy consumption, recyclability, and raw material use.')
    costumer_feedback = fields.Text(string='Costumer Feedback',
                                    help='Feedback or reviews received from early adopters or key customers after product launch.')

    @api.depends('introduction_date', 'supplier_id8')
    def _compute_innovation_rate(self):
        for record in self:
            # Assuming innovation rate is based on the number of product introductions over a fixed period (e.g., last year).
            recent_products = self.search([
                ('supplier_id8', '=', record.supplier_id8.id),
                ('introduction_date', '>=', fields.Date.today() - timedelta(days=365))
            ])
            # E.g., new products per month on average.
            record.innovation_rate = len(recent_products) / 12.0

    _sql_constraints = [
        ('unique_supplier_product_innovation', 'UNIQUE(supplier_id8, product_id)',
         'Each product introduction must be unique per supplier.')
    ]

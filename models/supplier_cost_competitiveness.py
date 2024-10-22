from odoo import models, fields, api


class SupplierCostCompetitiveness(models.Model):
    _name = 'scm.supplier_cost_competitiveness'
    _description = 'Supplier Cost Competitiveness Indicators'

    supplier_id10 = fields.Many2one(
        'scm.supplier', string='Supplier', ondelete='cascade', required=True)
    product_id = fields.Many2one('product.product', string='Product',
                                 required=True, help='Product or service being supplied.')

    # Price Competitiveness
    supplier_price = fields.Float(string='Supplier Price', required=True,
                                  help='Price offered by the supplier for the product or service.')
    market_average_price = fields.Float(
        string='Market Average Price', required=True, help='Average market price for the product or service.')
    price_competitiveness_index = fields.Float(string='Price Competitiveness Index', compute='_compute_price_competitiveness',
                                               store=True, help='Computed index of the supplier price compared to the market average.')

    # Total Cost of Ownership (TCO)
    procurement_cost = fields.Float(
        string='Procurement Cost', required=True, help='Cost of purchasing the product or service.')
    operation_cost = fields.Float(string='Operation Cost', required=True,
                                  help='Cost of operating or using the product over its lifecycle.')
    maintenance_cost = fields.Float(
        string='Maintenance Cost', help='Estimated cost for maintaining the product over its lifecycle.')
    disposal_cost = fields.Float(
        string='Disposal Cost', help='Cost associated with disposing of the product at the end of its useful life.')
    total_cost_of_ownership = fields.Float(string='Total Cost of Ownership (TCO)', compute='_compute_tco',
                                           store=True, help='Comprehensive cost analysis over the entire lifecycle of the product.')

    # Price Trend Over Time
    price_trend = fields.Float(string='Price Trend (%)',
                               help='Percentage change in the supplier\'s price over a defined period, showing price stability or volatility.')

    # Custom Constraint: Unique Price Comparison
    _sql_constraints = [
        ('unique_supplier_product_price', 'UNIQUE(supplier_id10, product_id)',
         'Each supplier and product combination must have unique pricing details.')
    ]

    @api.depends('supplier_price', 'market_average_price')
    def _compute_price_competitiveness(self):
        for record in self:
            if record.market_average_price:
                record.price_competitiveness_index = (
                    record.supplier_price / record.market_average_price) * 100
            else:
                record.price_competitiveness_index = 0.0

    @api.depends('procurement_cost', 'operation_cost', 'maintenance_cost', 'disposal_cost')
    def _compute_tco(self):
        for record in self:
            record.total_cost_of_ownership = sum([
                record.procurement_cost,
                record.operation_cost,
                record.maintenance_cost or 0.0,  # Handle optional fields
                record.disposal_cost or 0.0
            ])

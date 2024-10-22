from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta

class TestSupplierProductInnovation(TransactionCase):

    def setUp(self):
        super(TestSupplierProductInnovation, self).setUp()
        # Create related records for supplier, product, and category
        self.supplier = self.env['scm.supplier'].create({
            'name': 'Supplier A',
        })
        self.product = self.env['product.product'].create({
            'name': 'Product A',
        })
        self.product_category = self.env['product.category'].create({
            'name': 'Category A',
        })

    def test_innovation_creation(self):
        innovation = self.env['scm.supplier_product_innovation'].create({
            'supplier_id8': self.supplier.id,
            'product_id': self.product.id,
            'introduction_date': '2024-01-01',
            'product_category_id': self.product_category.id,
            'innovation_type': 'radical',
            'development_time': 12.0,
            'market_impact': 'high',
            'patent_filed': True,
            'sustainability_index': 8.5,
            'costumer_feedback': 'Great innovation with promising market impact.',
        })
        self.assertEqual(innovation.supplier_id8.id, self.supplier.id)
        self.assertEqual(innovation.product_id.id, self.product.id)
        self.assertEqual(innovation.innovation_type, 'radical')
        self.assertTrue(innovation.patent_filed)

    def test_unique_supplier_product_innovation_constraint(self):
        self.env['scm.supplier_product_innovation'].create({
            'supplier_id8': self.supplier.id,
            'product_id': self.product.id,
            'introduction_date': '2024-01-01',
        })
        with self.assertRaises(ValidationError):
            self.env['scm.supplier_product_innovation'].create({
                'supplier_id8': self.supplier.id,
                'product_id': self.product.id,  # Same supplier and product
                'introduction_date': '2024-05-01',
            })

    def test_innovation_rate_computation(self):
        # Create a product innovation introduced within the past year
        self.env['scm.supplier_product_innovation'].create({
            'supplier_id8': self.supplier.id,
            'product_id': self.product.id,
            'introduction_date': fields.Date.today() - timedelta(days=100),
        })
        # Create a second product innovation from the same supplier
        self.env['scm.supplier_product_innovation'].create({
            'supplier_id8': self.supplier.id,
            'product_id': self.env['product.product'].create({'name': 'Product B'}).id,
            'introduction_date': fields.Date.today() - timedelta(days=50),
        })

        innovation_rate = self.env['scm.supplier_product_innovation'].search([
            ('supplier_id8', '=', self.supplier.id)
        ]).mapped('innovation_rate')

        # Check the innovation rate is correctly calculated (2 innovations in the last year)
        for rate in innovation_rate:
            self.assertEqual(rate, 2 / 12.0)

    def test_innovation_rate_no_recent_innovations(self):
        # Create an innovation introduced more than a year ago
        self.env['scm.supplier_product_innovation'].create({
            'supplier_id8': self.supplier.id,
            'product_id': self.product.id,
            'introduction_date': fields.Date.today() - timedelta(days=400),
        })

        # Check the innovation rate is 0 (no innovations in the last year)
        innovation_rate = self.env['scm.supplier_product_innovation'].search([
            ('supplier_id8', '=', self.supplier.id)
        ]).mapped('innovation_rate')

        for rate in innovation_rate:
            self.assertEqual(rate, 0)

    def test_positive_sustainability_index(self):
        # Ensure sustainability index can be set correctly
        innovation = self.env['scm.supplier_product_innovation'].create({
            'supplier_id8': self.supplier.id,
            'product_id': self.product.id,
            'introduction_date': fields.Date.today(),
            'sustainability_index': 9.0
        })
        self.assertEqual(innovation.sustainability_index, 9.0)

    def test_default_fields(self):
        # Test default field values
        innovation = self.env['scm.supplier_product_innovation'].create({
            'supplier_id8': self.supplier.id,
            'product_id': self.product.id,
            'introduction_date': fields.Date.today(),
        })
        self.assertTrue(innovation.patent_filed is False)  # Default should be False
        self.assertEqual(innovation.market_impact, False)  # No default set

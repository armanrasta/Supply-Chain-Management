from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError


class TestSupplierCostCompetitiveness(TransactionCase):

    def setUp(self):
        super(TestSupplierCostCompetitiveness, self).setUp()
        self.supplier = self.env['scm.supplier'].create({
            'name': 'Test Supplier',
            'contact_email': 'test@supplier.com',
            'contact_phone': '123456789',
            'address': '123 Supplier Lane',
            'performance_score': 3.5,
        })
        self.product = self.env['product.product'].create({
            'name': 'Test Product',
            'list_price': 100.0,
            'standard_price': 80.0
        })

    def test_create_cost_competitiveness(self):
        # Create a valid cost competitiveness record
        cost_record = self.env['scm.supplier_cost_competitiveness'].create({
            'supplier_id10': self.supplier.id,
            'product_id': self.product.id,
            'supplier_price': 90.0,
            'market_average_price': 100.0,
            'procurement_cost': 85.0,
            'operation_cost': 10.0,
            'maintenance_cost': 5.0,
            'disposal_cost': 2.0,
        })
        self.assertEqual(cost_record.supplier_price, 90.0)
        self.assertEqual(cost_record.total_cost_of_ownership, 102.0)

    def test_compute_price_competitiveness(self):
        # Create a record and compute the price competitiveness index
        cost_record = self.env['scm.supplier_cost_competitiveness'].create({
            'supplier_id10': self.supplier.id,
            'product_id': self.product.id,
            'supplier_price': 80.0,
            'market_average_price': 100.0,
            'procurement_cost': 80.0,
            'operation_cost': 20.0,
        })
        cost_record._compute_price_competitiveness()
        expected_index = (80 / 100) * 100  # Should be 80
        self.assertAlmostEqual(cost_record.price_competitiveness_index, expected_index)

    def test_unique_supplier_product_price_constraint(self):
        # Create the first record
        self.env['scm.supplier_cost_competitiveness'].create({
            'supplier_id10': self.supplier.id,
            'product_id': self.product.id,
            'supplier_price': 90.0,
            'market_average_price': 100.0,
        })

        # Try to create another record with the same supplier and product (should fail)
        with self.assertRaises(ValidationError):
            self.env['scm.supplier_cost_competitiveness'].create({
                'supplier_id10': self.supplier.id,
                'product_id': self.product.id,
                'supplier_price': 85.0,
                'market_average_price': 100.0,
            })

    def test_invalid_price_trend(self):
        # Test invalid price trends
        with self.assertRaises(ValidationError):
            self.env['scm.supplier_cost_competitiveness'].create({
                'supplier_id10': self.supplier.id,
                'product_id': self.product.id,
                'supplier_price': 90.0,
                'market_average_price': 100.0,
                'price_trend': -105.0,  # Invalid: trend cannot be less than -100%
            })

        with self.assertRaises(ValidationError):
            self.env['scm.supplier_cost_competitiveness'].create({
                'supplier_id10': self.supplier.id,
                'product_id': self.product.id,
                'supplier_price': 90.0,
                'market_average_price': 100.0,
                'price_trend': 105.0,  # Invalid: trend cannot be greater than 100%
            })

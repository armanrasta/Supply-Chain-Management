from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError


class TestSupplierCapacity(TransactionCase):

    def setUp(self):
        super(TestSupplierCapacity, self).setUp()
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

    def test_create_capacity(self):
        # Create a valid capacity record
        capacity = self.env['scm.supplier_capacity'].create({
            'supplier_id5': self.supplier.id,
            'product_id': self.product.id,
            'max_capacity': 1000,
            'min_capacity': 500,
            'current_utilization': 75.0,
            'utilization_trend': 5.0,
            'lead_time': 10,
            'capacity_type': 'normal',
            'capacity_status': 'stable',
            'period': 'monthly',
        })
        self.assertEqual(capacity.max_capacity, 1000)
        self.assertEqual(capacity.current_utilization, 75.0)
    
    def test_unique_supplier_product_period_constraint(self):
        # Create the first capacity record
        self.env['scm.supplier_capacity'].create({
            'supplier_id5': self.supplier.id,
            'product_id': self.product.id,
            'max_capacity': 1000,
            'min_capacity': 500,
            'current_utilization': 80.0,
            'period': 'monthly',
        })
        # Try to create a second record with the same supplier, product, and period (should fail)
        with self.assertRaises(ValidationError):
            self.env['scm.supplier_capacity'].create({
                'supplier_id5': self.supplier.id,
                'product_id': self.product.id,
                'max_capacity': 1200,
                'min_capacity': 600,
                'current_utilization': 85.0,
                'period': 'monthly',
            })

    def test_invalid_utilization(self):
        # Test invalid utilization values
        with self.assertRaises(ValidationError):
            self.env['scm.supplier_capacity'].create({
                'supplier_id5': self.supplier.id,
                'product_id': self.product.id,
                'current_utilization': 110.0,  # Invalid: >100%
            })

        with self.assertRaises(ValidationError):
            self.env['scm.supplier_capacity'].create({
                'supplier_id5': self.supplier.id,
                'product_id': self.product.id,
                'current_utilization': -5.0,  # Invalid: negative
            })

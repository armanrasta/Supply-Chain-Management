from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError

class TestSupplierReliability(TransactionCase):

    def setUp(self):
        super(TestSupplierReliability, self).setUp()
        self.supplier = self.env['scm.supplier'].create({
            'name': 'Supplier 2'
        })

    def test_create_supplier_reliability(self):
        """Test creation of supplier reliability record."""
        reliability = self.env['scm.supplier_reliability'].create({
            'supplier_id2': self.supplier.id,
            'on_time_delivery': 90.0,
            'quality': 85.0,
            'responsiveness': 80.0,
        })
        self.assertTrue(reliability, "Supplier reliability record should be created successfully.")
        self.assertEqual(reliability.overall_reliability, 85.0, "Overall reliability should be the average of the three scores.")

    def test_unique_constraint(self):
        """Test unique constraint on supplier and date."""
        self.env['scm.supplier_reliability'].create({
            'supplier_id2': self.supplier.id,
            'on_time_delivery': 90.0,
            'quality': 85.0,
            'responsiveness': 80.0,
        })

        with self.assertRaises(ValidationError):
            self.env['scm.supplier_reliability'].create({
                'supplier_id2': self.supplier.id,
                'on_time_delivery': 92.0,
                'quality': 88.0,
                'responsiveness': 82.0,
            })

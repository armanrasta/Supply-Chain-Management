from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError

class TestScalabilityPlans(TransactionCase):

    def setUp(self):
        super(TestScalabilityPlans, self).setUp()
        self.supplier = self.env['scm.supplier'].create({
            'name': 'Supplier 1'
        })

    def test_create_scalability_plan(self):
        """Test creation of scalability plan for a supplier."""
        scalability_plan = self.env['scm.supplier_scalability'].create({
            'supplier_id6': self.supplier.id,
            'scale_up_plan': 'Increase production by 30% in 2 months',
            'scale_down_plan': 'Reduce production by 20% in 1 month',
            'investment_required': 50000,
            'time_to_scale_up': 60,
            'time_to_scale_down': 30,
            'scale_up_capacity': 30.0,
            'scale_down_capacity': 20.0,
        })
        self.assertTrue(scalability_plan, "Scalability plan should be created successfully.")

    def test_unique_constraint(self):
        """Test unique constraint for a scalability plan per supplier."""
        self.env['scm.supplier_scalability'].create({
            'supplier_id6': self.supplier.id,
            'scale_up_plan': 'Increase production by 30% in 2 months',
        })

        with self.assertRaises(ValidationError):
            self.env['scm.supplier_scalability'].create({
                'supplier_id6': self.supplier.id,
                'scale_up_plan': 'Another plan',
            })

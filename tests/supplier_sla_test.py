from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError

class TestSLA(TransactionCase):

    def setUp(self):
        super(TestSLA, self).setUp()

    def test_create_sla(self):
        """Test creation of an SLA."""
        sla = self.env['scm.sla'].create({
            'name': 'Basic SLA',
            'fulfillment_rate': 95.0,
            'delivery_time': 5,
            'support_response_time': 48,
        })
        self.assertTrue(sla, "SLA should be created successfully.")

    def test_unique_sla_name(self):
        """Test unique constraint on SLA name."""
        self.env['scm.sla'].create({
            'name': 'Basic SLA',
            'fulfillment_rate': 95.0,
        })

        with self.assertRaises(ValidationError):
            self.env['scm.sla'].create({
                'name': 'Basic SLA',  # Same name
                'fulfillment_rate': 90.0,
            })

from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError

class TestTradeOffWeight(TransactionCase):

    def setUp(self):
        super(TestTradeOffWeight, self).setUp()
        # Setting up initial data for testing
        self.tradeoff_weight_1 = self.env['scm.tradeoff_weight'].create({
            'name': 'Standard Weight',
            'cost_weight': 1.0,
            'service_weight': 1.0,
            'description': 'Standard trade-off weight for cost and service metrics.',
            'active': True,
        })

    def test_tradeoff_weight_creation(self):
        # Test if a trade-off weight record is created correctly
        self.assertEqual(self.tradeoff_weight_1.name, 'Standard Weight')
        self.assertEqual(self.tradeoff_weight_1.cost_weight, 1.0)
        self.assertEqual(self.tradeoff_weight_1.service_weight, 1.0)
        self.assertEqual(self.tradeoff_weight_1.description, 'Standard trade-off weight for cost and service metrics.')
        self.assertTrue(self.tradeoff_weight_1.active)

    def test_unique_weight_name_constraint(self):
        # Test unique constraint on the weight name
        with self.assertRaises(ValidationError):
            self.env['scm.tradeoff_weight'].create({
                'name': 'Standard Weight',  # Duplicate name
                'cost_weight': 2.0,
                'service_weight': 2.0,
            })

    def test_default_weights(self):
        # Test the default weights upon creation
        tradeoff_weight_2 = self.env['scm.tradeoff_weight'].create({
            'name': 'Default Weights Test'
        })
        self.assertEqual(tradeoff_weight_2.cost_weight, 1.0)  # Default value
        self.assertEqual(tradeoff_weight_2.service_weight, 1.0)  # Default value

    def test_active_state(self):
        # Test the active state functionality
        self.assertTrue(self.tradeoff_weight_1.active)

        # Deactivate the trade-off weight
        self.tradeoff_weight_1.active = False
        self.assertFalse(self.tradeoff_weight_1.active)

        # Reactivate the trade-off weight
        self.tradeoff_weight_1.active = True
        self.assertTrue(self.tradeoff_weight_1.active)

    def test_description_field(self):
        # Test that the description field can be updated
        self.tradeoff_weight_1.description = 'Updated description for the trade-off weight.'
        self.assertEqual(self.tradeoff_weight_1.description, 'Updated description for the trade-off weight.')


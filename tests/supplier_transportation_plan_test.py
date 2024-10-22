from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError

class TestTransportationPlan(TransactionCase):

    def setUp(self):
        super(TestTransportationPlan, self).setUp()
        # Create initial data for testing
        self.transportation_mode = self.env['scm.transportation_mode'].create({
            'name': 'Air Freight',
            'availability_probability': 95.0,
            'description': 'Fast and reliable air freight transportation.',
        })

        self.tradeoff_weight = self.env['scm.tradeoff_weight'].create({
            'name': 'Cost vs Service Weight A',
            'cost_weight': 0.7,
            'service_weight': 0.3,
            'description': 'Trade-off prioritizing cost over service.',
        })

        self.transportation_plan = self.env['scm.transportation_plan'].create({
            'name': 'Plan A',
            'transportation_mode_id': self.transportation_mode.id,
            'tradeoff_weight_id': self.tradeoff_weight.id,
        })

    def test_transportation_plan_creation(self):
        # Test if the transportation plan record is created correctly
        self.assertEqual(self.transportation_plan.name, 'Plan A')
        self.assertEqual(self.transportation_plan.transportation_mode_id, self.transportation_mode)
        self.assertEqual(self.transportation_plan.tradeoff_weight_id, self.tradeoff_weight)

    def test_unique_plan_name_constraint(self):
        # Test unique constraint on the transportation plan name
        with self.assertRaises(ValidationError):
            self.env['scm.transportation_plan'].create({
                'name': 'Plan A',  # Duplicate name
                'transportation_mode_id': self.transportation_mode.id,
                'tradeoff_weight_id': self.tradeoff_weight.id,
            })

    def test_transportation_mode_relationship(self):
        # Test if the transportation plan is linked correctly to a transportation mode
        transportation_mode_2 = self.env['scm.transportation_mode'].create({
            'name': 'Sea Freight',
            'availability_probability': 85.0,
        })

        transportation_plan_2 = self.env['scm.transportation_plan'].create({
            'name': 'Plan B',
            'transportation_mode_id': transportation_mode_2.id,
            'tradeoff_weight_id': self.tradeoff_weight.id,
        })

        self.assertEqual(transportation_plan_2.transportation_mode_id, transportation_mode_2)
        self.assertEqual(transportation_plan_2.transportation_mode_id.name, 'Sea Freight')

    def test_tradeoff_weight_relationship(self):
        # Test if the transportation plan is linked correctly to a trade-off weight
        tradeoff_weight_2 = self.env['scm.tradeoff_weight'].create({
            'name': 'Cost vs Service Weight B',
            'cost_weight': 0.4,
            'service_weight': 0.6,
        })

        transportation_plan_3 = self.env['scm.transportation_plan'].create({
            'name': 'Plan C',
            'transportation_mode_id': self.transportation_mode.id,
            'tradeoff_weight_id': tradeoff_weight_2.id,
        })

        self.assertEqual(transportation_plan_3.tradeoff_weight_id, tradeoff_weight_2)
        self.assertEqual(transportation_plan_3.tradeoff_weight_id.name, 'Cost vs Service Weight B')

    def test_missing_required_fields(self):
        # Test that creating a transportation plan without required fields raises an error
        with self.assertRaises(ValidationError):
            self.env['scm.transportation_plan'].create({
                'name': 'Invalid Plan',  # Missing transportation_mode_id and tradeoff_weight_id
            })

    def test_name_field_update(self):
        # Test updating the name field of the transportation plan
        self.transportation_plan.name = 'Updated Plan A'
        self.assertEqual(self.transportation_plan.name, 'Updated Plan A')

    def test_transportation_mode_update(self):
        # Test updating the transportation mode of an existing transportation plan
        new_transportation_mode = self.env['scm.transportation_mode'].create({
            'name': 'Rail Freight',
            'availability_probability': 90.0,
        })

        self.transportation_plan.transportation_mode_id = new_transportation_mode
        self.assertEqual(self.transportation_plan.transportation_mode_id, new_transportation_mode)
        self.assertEqual(self.transportation_plan.transportation_mode_id.name, 'Rail Freight')

    def test_tradeoff_weight_update(self):
        # Test updating the trade-off weight of an existing transportation plan
        new_tradeoff_weight = self.env['scm.tradeoff_weight'].create({
            'name': 'Balanced Cost vs Service',
            'cost_weight': 0.5,
            'service_weight': 0.5,
        })

        self.transportation_plan.tradeoff_weight_id = new_tradeoff_weight
        self.assertEqual(self.transportation_plan.tradeoff_weight_id, new_tradeoff_weight)
        self.assertEqual(self.transportation_plan.tradeoff_weight_id.name, 'Balanced Cost vs Service')

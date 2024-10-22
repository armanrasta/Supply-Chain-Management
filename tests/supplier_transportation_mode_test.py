from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError

class TestTransportationMode(TransactionCase):

    def setUp(self):
        super(TestTransportationMode, self).setUp()
        # Create initial data for testing
        self.network_robustness = self.env['scm.network_robustness'].create({
            'name': 'Robust Network A',
            'description': 'A description for a robust network.',
        })
        self.transportation_mode_1 = self.env['scm.transportation_mode'].create({
            'name': 'Air Freight',
            'availability_probability': 90.0,
            'description': 'Fast delivery via air transport.',
            'active': True,
        })

    def test_transportation_mode_creation(self):
        # Test if a transportation mode record is created correctly
        self.assertEqual(self.transportation_mode_1.name, 'Air Freight')
        self.assertEqual(self.transportation_mode_1.availability_probability, 90.0)
        self.assertEqual(self.transportation_mode_1.description, 'Fast delivery via air transport.')
        self.assertTrue(self.transportation_mode_1.active)

    def test_unique_transport_mode_constraint(self):
        # Test unique constraint on the transportation mode name
        with self.assertRaises(ValidationError):
            self.env['scm.transportation_mode'].create({
                'name': 'Air Freight',  # Duplicate name
                'availability_probability': 85.0,
            })

    def test_default_availability_probability(self):
        # Test that new transportation modes have a default availability probability
        transportation_mode_2 = self.env['scm.transportation_mode'].create({
            'name': 'Sea Freight'
        })
        self.assertEqual(transportation_mode_2.availability_probability, 100.0)  # Default value

    def test_active_state(self):
        # Test the active state functionality
        self.assertTrue(self.transportation_mode_1.active)

        # Deactivate the transportation mode
        self.transportation_mode_1.active = False
        self.assertFalse(self.transportation_mode_1.active)

        # Reactivate the transportation mode
        self.transportation_mode_1.active = True
        self.assertTrue(self.transportation_mode_1.active)

    def test_network_robustness_relationship(self):
        # Test the many-to-many relationship with network robustness
        self.transportation_mode_1.network_robustness_id = [(4, self.network_robustness.id)]

        # Check if the relationship is established correctly
        self.assertIn(self.network_robustness, self.transportation_mode_1.network_robustness_id)

    def test_description_field(self):
        # Test that the description field can be updated
        self.transportation_mode_1.description = 'Updated description for air freight.'
        self.assertEqual(self.transportation_mode_1.description, 'Updated description for air freight.')

    def test_create_inactive_mode(self):
        # Test creating an inactive transportation mode
        transportation_mode_3 = self.env['scm.transportation_mode'].create({
            'name': 'Rail Transport',
            'active': False
        })
        self.assertFalse(transportation_mode_3.active)


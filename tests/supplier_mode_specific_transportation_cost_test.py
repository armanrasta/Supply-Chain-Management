from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError


class TestModeSpecificTransportationCost(TransactionCase):

    def setUp(self):
        super(TestModeSpecificTransportationCost, self).setUp()
        # Create necessary related records for tests
        self.transport_mode = self.env['scm.transportation_mode'].create({
            'name': 'Air Freight',
            'availability_probability': 95.0,
            'description': 'Fast and reliable air freight transportation.',
        })

        self.carrier = self.env['res.partner'].create({
            'name': 'Global Logistics',
            'supplier': True,
            'is_company': True,
        })

        self.transportation_cost = self.env['scm.mode_specific_transportation_cost'].create({
            'transport_mode_id': self.transport_mode.id,
            'carrier_id': self.carrier.id,
            'date_effective': '2024-10-01',
            'cost_per_km': 10.50,
            'cost_per_hour': 45.00,
            'fixed_cost': 500.00,
            'variable_cost_percentage': 20.0,
        })

    def test_transportation_cost_creation(self):
        # Test creation of transportation cost record
        self.assertEqual(self.transportation_cost.transport_mode_id, self.transport_mode)
        self.assertEqual(self.transportation_cost.carrier_id, self.carrier)
        self.assertEqual(self.transportation_cost.cost_per_km, 10.50)
        self.assertEqual(self.transportation_cost.cost_per_hour, 45.00)
        self.assertEqual(self.transportation_cost.fixed_cost, 500.00)
        self.assertEqual(self.transportation_cost.variable_cost_percentage, 20.0)

    def test_unique_mode_carrier_date_constraint(self):
        # Test unique constraint for transport_mode_id, carrier_id, and date_effective
        with self.assertRaises(ValidationError):
            self.env['scm.mode_specific_transportation_cost'].create({
                'transport_mode_id': self.transport_mode.id,
                'carrier_id': self.carrier.id,
                'date_effective': '2024-10-01',  # Same date
                'cost_per_km': 12.00,
                'cost_per_hour': 50.00,
                'fixed_cost': 600.00,
                'variable_cost_percentage': 25.0,
            })

    def test_positive_costs_constraint(self):
        # Test CHECK constraint for non-negative cost fields
        with self.assertRaises(ValidationError):
            self.env['scm.mode_specific_transportation_cost'].create({
                'transport_mode_id': self.transport_mode.id,
                'carrier_id': self.carrier.id,
                'date_effective': '2024-10-10',
                'cost_per_km': -5.00,  # Negative value should trigger the validation
                'cost_per_hour': 45.00,
                'fixed_cost': 500.00,
                'variable_cost_percentage': 10.0,
            })

    def test_variable_cost_percentage_constraint(self):
        # Test custom constraint for variable cost percentage (0 <= variable_cost_percentage <= 100)
        with self.assertRaises(ValidationError):
            self.transportation_cost.variable_cost_percentage = 120.0
            self.transportation_cost._check_variable_cost_percentage()

        with self.assertRaises(ValidationError):
            self.transportation_cost.variable_cost_percentage = -10.0
            self.transportation_cost._check_variable_cost_percentage()

    def test_update_transport_mode(self):
        # Test updating the transport mode field of the transportation cost
        new_transport_mode = self.env['scm.transportation_mode'].create({
            'name': 'Sea Freight',
            'availability_probability': 90.0,
        })
        self.transportation_cost.transport_mode_id = new_transport_mode
        self.assertEqual(self.transportation_cost.transport_mode_id, new_transport_mode)
        self.assertEqual(self.transportation_cost.transport_mode_id.name, 'Sea Freight')

    def test_update_cost_fields(self):
        # Test updating cost fields and ensuring values are updated correctly
        self.transportation_cost.cost_per_km = 15.00
        self.transportation_cost.cost_per_hour = 50.00
        self.assertEqual(self.transportation_cost.cost_per_km, 15.00)
        self.assertEqual(self.transportation_cost.cost_per_hour, 50.00)

    def test_missing_required_fields(self):
        # Test creating a record with missing required fields
        with self.assertRaises(ValidationError):
            self.env['scm.mode_specific_transportation_cost'].create({
                'transport_mode_id': self.transport_mode.id,
                # Missing carrier_id and costs should trigger validation errors
            })

    def test_date_effective_default(self):
        # Test that the default value for date_effective is today's date
        cost_record = self.env['scm.mode_specific_transportation_cost'].create({
            'transport_mode_id': self.transport_mode.id,
            'carrier_id': self.carrier.id,
            'cost_per_km': 12.00,
            'cost_per_hour': 50.00,
            'fixed_cost': 600.00,
            'variable_cost_percentage': 25.0,
        })
        self.assertEqual(cost_record.date_effective, fields.Date.today())

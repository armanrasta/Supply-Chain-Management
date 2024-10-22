from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta

class TestCarbonObjective(TransactionCase):

    def setUp(self):
        super(TestCarbonObjective, self).setUp()
        self.supplier = self.env['scm.supplier'].create({
            'name': 'Supplier 2',
        })
        self.inventory_item = self.env['scm.inventory_item'].create({
            'name': 'Test Inventory Item',
        })
        self.facility = self.env['scm.warehouse_location'].create({
            'name': 'Test Facility',
        })

    def test_create_carbon_objective(self):
        """Test creation of a carbon footprint reduction objective."""
        carbon_objective = self.env['scm.carbon_objective'].create({
            'name': 'Reduce CO2 Emissions',
            'description': 'Objective to reduce CO2 emissions by 30%',
            'target_reduction': 30.0,
            'start_date': fields.Date.today(),
            'end_date': fields.Date.today() + timedelta(days=365),
            'supplier_id4': [(6, 0, [self.supplier.id])],
            'inventory_item_id4': [(6, 0, [self.inventory_item.id])],
            'facility_ids': [(6, 0, [self.facility.id])],
        })
        self.assertTrue(carbon_objective, "Carbon objective should be created successfully.")
        self.assertEqual(carbon_objective.target_reduction, 30.0, "Target reduction should be 30%.")

    def test_carbon_objective_invalid_dates(self):
        """Test that carbon objective cannot be created with invalid dates."""
        with self.assertRaises(ValidationError):
            self.env['scm.carbon_objective'].create({
                'name': 'Invalid Date Objective',
                'target_reduction': 20.0,
                'start_date': fields.Date.today(),
                'end_date': fields.Date.today() - timedelta(days=10),  # End date is before start date
            })

    def test_add_suppliers_inventory_items_and_facilities(self):
        """Test adding related suppliers, inventory items, and facilities to a carbon objective."""
        carbon_objective = self.env['scm.carbon_objective'].create({
            'name': 'Test Carbon Objective',
            'target_reduction': 15.0,
            'start_date': fields.Date.today(),
            'end_date': fields.Date.today() + timedelta(days=180),
        })
        carbon_objective.write({
            'supplier_id4': [(6, 0, [self.supplier.id])],
            'inventory_item_id4': [(6, 0, [self.inventory_item.id])],
            'facility_ids': [(6, 0, [self.facility.id])],
        })
        self.assertIn(self.supplier.id, carbon_objective.supplier_id4.ids, "Supplier should be linked to the carbon objective.")
        self.assertIn(self.inventory_item.id, carbon_objective.inventory_item_id4.ids, "Inventory item should be linked to the carbon objective.")
        self.assertIn(self.facility.id, carbon_objective.facility_ids.ids, "Facility should be linked to the carbon objective.")

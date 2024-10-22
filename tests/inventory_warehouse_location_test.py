from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError
from datetime import timedelta

class TestWarehouseLocation(TransactionCase):

    def setUp(self):
        super(TestWarehouseLocation, self).setUp()
        # Create a warehouse for testing
        self.warehouse = self.env['stock.warehouse'].create({
            'name': 'Main Warehouse',
        })

        # Create a parent warehouse location
        self.parent_location = self.env['scm.warehouse_location'].create({
            'name': 'Parent Location',
            'warehouse_id': self.warehouse.id,
            'capacity': 100.0,  # capacity in cubic meters
            'address': '123 Parent St',
        })

        # Create a child warehouse location
        self.child_location = self.env['scm.warehouse_location'].create({
            'name': 'Child Location',
            'warehouse_id': self.warehouse.id,
            'parent_location_id': self.parent_location.id,
            'capacity': 50.0,  # capacity in cubic meters
            'address': '456 Child Ave',
        })

        # Create an inventory item to test utilization
        self.inventory_item = self.env['scm.inventory_item'].create({
            'name': 'Test Inventory Item',
            'location_id': self.child_location.id,
            'volume': 10.0,  # volume in cubic meters
            'stock_level': 3,  # 3 units in stock
        })

    def test_create_warehouse_location(self):
        """Test the creation of a warehouse location."""
        warehouse_location = self.env['scm.warehouse_location'].create({
            'name': "New Warehouse",
            'warehouse_id': self.warehouse.id,
            'capacity': 32000,
            'fixed_costs': 33.33,
            'address': '789 New St',
            'active': True,
        })
        self.assertTrue(warehouse_location, "Warehouse location should be created successfully.")
        self.assertEqual(warehouse_location.name, "New Warehouse", "Warehouse location name should be set correctly.")
        self.assertEqual(warehouse_location.capacity, 32000, "Capacity should be set correctly.")
        self.assertEqual(warehouse_location.fixed_costs, 33.33, "Fixed costs should be set correctly.")
        self.assertEqual(warehouse_location.address, '789 New St', "Address should be set correctly.")
    
    def test_compute_complete_name(self):
        """Test the computation of the complete name."""
        # The complete name should concatenate the parent and child names
        self.assertEqual(self.child_location.complete_name, 'Parent Location / Child Location',
                         "The complete name should include both parent and child names.")
    
    def test_compute_utilization(self):
        """Test the computation of utilization based on inventory volume."""
        # For the child location: utilization = (volume * stock_level) / capacity * 100
        # (10 * 3) / 50 = 60%
        self.assertAlmostEqual(self.child_location.utilization, 60.0,
                               msg="The utilization should be correctly calculated based on inventory.")
    
    def test_invalid_capacity(self):
        """Test that a warehouse location cannot have a negative capacity."""
        with self.assertRaises(ValidationError):
            self.env['scm.warehouse_location'].create({
                'name': 'Invalid Capacity Location',
                'warehouse_id': self.warehouse.id,
                'capacity': -100.0,  # Negative capacity
                'address': 'Invalid Address',
            })
    
    def test_warehouse_location_relation(self):
        """Test the parent-child relationship of warehouse locations."""
        self.assertEqual(self.child_location.parent_location_id, self.parent_location,
                         "The child location should be correctly linked to the parent location.")
        self.assertIn(self.child_location.id, self.parent_location.child_location_id.ids,
                      "The parent location should have the child location in its child locations.")
    
    def test_add_carbon_objectives(self):
        """Test the Many2many relationship with carbon objectives."""
        # Create a carbon objective
        carbon_objective = self.env['scm.carbon_objective'].create({
            'name': 'Reduce CO2 Emissions',
            'target_reduction': 25.0,
            'start_date': fields.Date.today(),
            'end_date': fields.Date.today() + timedelta(days=365),
        })
        
        # Link the carbon objective to the warehouse location
        self.child_location.write({
            'carbon_objective_ids': [(6, 0, [carbon_objective.id])],
        })

        # Check that the carbon objective was added
        self.assertIn(carbon_objective.id, self.child_location.carbon_objective_ids.ids,
                      "The carbon objective should be linked to the warehouse location.")
    
    def test_unique_location_name_constraint(self):
        """Test the unique constraint on warehouse location name."""
        with self.assertRaises(ValidationError):
            # Try to create another location with the same name as the parent
            self.env['scm.warehouse_location'].create({
                'name': 'Parent Location',  # Same name as parent_location
                'warehouse_id': self.warehouse.id,
                'capacity': 100.0,
                'address': '789 Duplicate St',
            })

    def test_delete_parent_location(self):
        """Test deletion of a parent location and the cascade effect."""
        self.parent_location.unlink()
        self.assertFalse(self.child_location.exists(),
                         "Child location should be deleted when parent location is unlinked.")

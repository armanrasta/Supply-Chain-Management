from odoo.tests import common
from odoo.exceptions import ValidationError


class TestInventoryItemCategory(common.TransactionCase):

    def setUp(self):
        super(TestInventoryItemCategory, self).setUp()
        # Create a main category
        self.main_category = self.env['scm.inventory_item_category'].create({
            'name': 'Main Category',
            'is_subcategory': False
        })
        
        # Create a sub-category
        self.sub_category = self.env['scm.inventory_item_category'].create({
            'name': 'Sub Category',
            'is_subcategory': True,
            'parent_id': self.main_category.id
        })

    def test_category_creation(self):
        """Test if category and subcategory are created correctly."""
        # Test if the main category was created successfully
        self.assertEqual(self.main_category.name, 'Main Category')
        self.assertFalse(self.main_category.is_subcategory)
        
        # Test if the subcategory was created and linked to the main category
        self.assertEqual(self.sub_category.name, 'Sub Category')
        self.assertTrue(self.sub_category.is_subcategory)
        self.assertEqual(self.sub_category.parent_id, self.main_category)

    def test_complete_name_computation(self):
        """Test if the complete name is correctly computed."""
        self.assertEqual(self.sub_category.complete_name, 'Main Category / Sub Category')

    def test_subcategory_constraint(self):
        """Test that a subcategory cannot be created without a parent."""
        with self.assertRaises(ValidationError):
            self.env['scm.inventory_item_category'].create({
                'name': 'Invalid Sub Category',
                'is_subcategory': True,
                'parent_id': False
            })

    def test_main_category_constraint(self):
        """Test that a main category cannot have a parent."""
        with self.assertRaises(ValidationError):
            self.env['scm.inventory_item_category'].create({
                'name': 'Invalid Main Category',
                'is_subcategory': False,
                'parent_id': self.main_category.id
            })

    def test_holding_cost(self):
        """Test the holding cost field."""
        category = self.env['scm.inventory_item_category'].create({
            'name': 'Holding Cost Category',
            'holding_cost': 10.0
        })
        self.assertEqual(category.holding_cost, 10.0)

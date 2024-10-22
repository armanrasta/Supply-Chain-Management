from odoo.tests.common import TransactionCase
from datetime import timedelta


class TestInventoryItem(TransactionCase):

    def setUp(self):
        super(TestInventoryItem, self).setUp()

        # Create a test supplier
        self.supplier = self.env['scm.supplier'].create({
            'name': 'Test Supplier',
        })

        # Create a test inventory item
        self.item = self.env['scm.inventory_item'].create({
            'name': 'Test Item',
            'description': 'This is a test inventory item.',
            'stock_level': 10,
            'reorder_point': 5,
            'safety_stock': 2,
            'lead_time_days': 7,
            'unit_cost': 100.0,
            'supplier_id13': [(6, 0, [self.supplier.id])]
        })

    def test_reorder_point_computation(self):
        """Test that the reorder point is correctly computed."""
        self.item.write({
            'demand_volatility': 10,
            'lead_time_days': 7,
            'lead_time_variability': 2,
        })
        self.item._compute_reorder_point()
        expected_reorder_point = (10 * 7) + (1.65 * 10 * (2 ** 0.5))
        self.assertEqual(self.item.reorder_point, expected_reorder_point, "Reorder point calculation failed.")

    def test_needs_reorder(self):
        """Test that the reorder flag is correctly computed."""
        self.item.write({'stock_level': 6})
        self.item._compute_needs_reorder()
        self.assertFalse(self.item.needs_reorder, "Item should not need reorder yet.")
        
        self.item.write({'stock_level': 4})
        self.item._compute_needs_reorder()
        self.assertTrue(self.item.needs_reorder, "Item should need reorder now.")

    def test_adjust_stock(self):
        """Test the stock adjustment logic."""
        self.item.adjust_stock(5)
        self.assertEqual(self.item.stock_level, 15, "Stock adjustment failed.")

        self.item.adjust_stock(-3)
        self.assertEqual(self.item.stock_level, 12, "Stock reduction failed.")

    def test_notify_upcoming_expirations(self):
        """Test the notification logic for upcoming expirations."""
        lot = self.env['scm.lot'].create({
            'name': 'Lot 001',
            'expiry_date': fields.Date.today() + timedelta(days=15),
            'lot_inventory_item_id': self.item.id,
        })
        self.item.notify_upcoming_expirations()
        # Check if an email has been sent (you might need to mock email sending for full verification)


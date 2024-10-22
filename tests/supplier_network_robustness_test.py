from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError


class TestNetworkRobustness(TransactionCase):

    def setUp(self):
        super(TestNetworkRobustness, self).setUp()
        self.transport_mode = self.env['scm.transportation_mode'].create({
            'name': 'Sea Freight',
            'availability_probability': 90.0,
        })
        self.inventory_item = self.env['scm.inventory_item'].create({
            'name': 'Product B',
            'description': 'Product with robustness metric',
        })
        self.supplier = self.env['scm.supplier'].create({
            'name': 'Supplier B',
        })

    def test_robustness_creation(self):
        robustness = self.env['scm.network_robustness'].create({
            'name': 'Supply Chain Flexibility',
            'description': 'Robustness parameter for flexibility.',
            'value': 85.0,
            'inventory_item_id3': [(6, 0, [self.inventory_item.id])],
            'transportation_mode_id': [(6, 0, [self.transport_mode.id])],
            'supplier_id': [(6, 0, [self.supplier.id])]
        })
        self.assertEqual(robustness.value, 85.0)
        self.assertTrue(self.inventory_item in robustness.inventory_item_id3)
        self.assertTrue(self.transport_mode in robustness.transportation_mode_id)
        self.assertTrue(self.supplier in robustness.supplier_id)

    def test_unique_parameter_name_constraint(self):
        self.env['scm.network_robustness'].create({
            'name': 'Cost Efficiency',
            'description': 'Parameter for cost efficiency.',
            'value': 75.0
        })
        with self.assertRaises(ValidationError):
            self.env['scm.network_robustness'].create({
                'name': 'Cost Efficiency',  # Same name should raise error
                'description': 'Another entry with the same name.',
                'value': 70.0
            })

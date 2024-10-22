from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError


class TestDemandForecast(TransactionCase):

    def setUp(self):
        super(TestDemandForecast, self).setUp()
        # Create related records
        self.inventory_item = self.env['scm.inventory_item'].create({
            'name': 'Item A',
            'description': 'Inventory item for demand forecasting',
        })
        self.supplier = self.env['scm.supplier'].create({
            'name': 'Supplier A',
        })

    def test_demand_forecast_creation(self):
        forecast = self.env['scm.demand_forecast'].create({
            'inventory_item_id2': self.inventory_item.id,
            'scenario': 'best',
            'period_start_date': '2024-11-01',
            'period_end_date': '2024-11-30',
            'forecasted_quantity': 100,
            'supplier_id3': self.supplier.id
        })
        self.assertEqual(forecast.scenario, 'best')
        self.assertEqual(forecast.forecasted_quantity, 100)

    def test_unique_item_scenario_period_constraint(self):
        self.env['scm.demand_forecast'].create({
            'inventory_item_id2': self.inventory_item.id,
            'scenario': 'best',
            'period_start_date': '2024-11-01',
            'period_end_date': '2024-11-30',
            'forecasted_quantity': 100,
            'supplier_id3': self.supplier.id
        })
        with self.assertRaises(ValidationError):
            self.env['scm.demand_forecast'].create({
                'inventory_item_id2': self.inventory_item.id,
                'scenario': 'best',
                'period_start_date': '2024-11-01',  # Same period, same scenario
                'period_end_date': '2024-11-30',
                'forecasted_quantity': 200,
                'supplier_id3': self.supplier.id
            })

    def test_period_dates_constraint(self):
        with self.assertRaises(ValidationError):
            self.env['scm.demand_forecast'].create({
                'inventory_item_id2': self.inventory_item.id,
                'scenario': 'worst',
                'period_start_date': '2024-12-01',
                'period_end_date': '2024-11-30',  # End date before start date
                'forecasted_quantity': 150,
                'supplier_id3': self.supplier.id
            })
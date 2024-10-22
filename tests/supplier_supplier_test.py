from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError


class TestSupplierModel(TransactionCase):

    def setUp(self):
        super(TestSupplierModel, self).setUp()
        # Create some sample records for testing purposes
        self.supplier = self.env['scm.supplier'].create({
            'name': 'Test Supplier',
            'contact_email': 'test@supplier.com',
            'contact_phone': '123456789',
            'address': '123 Supplier Lane',
            'performance_score': 3.5,
        })

        self.reliability_record_1 = self.env['scm.supplier_reliability'].create({
            'supplier_id2': self.supplier.id,
            'overall_reliability': 4.0
        })
        self.reliability_record_2 = self.env['scm.supplier_reliability'].create({
            'supplier_id2': self.supplier.id,
            'overall_reliability': 5.0
        })

        self.carbon_objective = self.env['scm.carbon_objective'].create({
            'name': 'Reduce Emissions',
            'target_percentage': 10.0
        })

        self.network_robustness = self.env['scm.network_robustness'].create({
            'parameter': 'High Redundancy',
            'score': 4.5
        })

    def test_supplier_creation(self):
        # Ensure the supplier record is created correctly
        self.assertEqual(self.supplier.name, 'Test Supplier')
        self.assertEqual(self.supplier.contact_email, 'test@supplier.com')
        self.assertTrue(self.supplier.active)

    def test_performance_score_computation(self):
        # Test the computed field `performance_score`
        self.supplier._compute_performance_score()
        self.assertEqual(self.supplier.performance_score,
                         4.5)  # Average of 4.0 and 5.0

    def test_invalid_performance_score(self):
        # Test that performance score constraints work
        with self.assertRaises(ValidationError):
            # Invalid score (greater than 5)
            self.supplier.write({'performance_score': 6})

        with self.assertRaises(ValidationError):
            # Invalid score (less than 0)
            self.supplier.write({'performance_score': -1})

    def test_reliability_relation(self):
        # Ensure that reliability records are correctly linked
        self.assertEqual(len(self.supplier.reliability_id), 2)
        reliability_scores = [
            rel.overall_reliability for rel in self.supplier.reliability_id]
        self.assertIn(4.0, reliability_scores)
        self.assertIn(5.0, reliability_scores)

    def test_carbon_objectives_relation(self):
        # Test Many2many relation for carbon objectives
        self.supplier.write(
            {'carbon_objective_id': [(4, self.carbon_objective.id)]})
        self.assertIn(self.carbon_objective, self.supplier.carbon_objective_id)

    def test_network_robustness_relation(self):
        # Test Many2many relation for network robustness
        self.supplier.write(
            {'network_robustness_id': [(4, self.network_robustness.id)]})
        self.assertIn(self.network_robustness,
                      self.supplier.network_robustness_id)

    def test_contact_persons_relation(self):
        # Test One2many relation for contact persons
        contact_person = self.env['scm.supplier_contact_person'].create({
            'supplier_id1': self.supplier.id,
            'name': 'Contact Person 1',
            'email': 'contact1@supplier.com',
            'phone': '987654321'
        })
        self.assertEqual(self.supplier.contact_person_id[0], contact_person)

    def test_scalability_relation(self):
        # Test One2many relation for scalability plans
        scalability = self.env['scm.supplier_scalability'].create({
            'supplier_id6': self.supplier.id,
            'scalability_factor': 'Increase Capacity',
            'plan_description': 'Expand production by 20%'
        })
        self.assertEqual(self.supplier.scalability_id[0], scalability)

    def test_demand_forecasts_relation(self):
        # Test One2many relation for demand forecasts
        forecast = self.env['scm.demand_forecast'].create({
            'supplier_id3': self.supplier.id,
            'forecast_value': 1000,
            'forecast_period': '2024-Q1'
        })
        self.assertEqual(self.supplier.demand_forecast_id[0], forecast)

    def test_inventory_items_relation(self):
        # Test Many2many relation for inventory items
        inventory_item = self.env['scm.inventory_item'].create({
            'name': 'Item A',
            'quantity': 100,
            'location': 'Warehouse 1'
        })
        self.supplier.write({'inventory_item_id': [(4, inventory_item.id)]})
        self.assertIn(inventory_item, self.supplier.inventory_item_id)

    def test_supplier_cost_competitiveness_relation(self):
        # Test One2many relation for cost competitiveness
        cost_competitive = self.env['scm.supplier_cost_competitiveness'].create({
            'supplier_id10': self.supplier.id,
            'cost_score': 3.5,
            'comment': 'Competitive pricing'
        })
        self.assertEqual(
            self.supplier.supplier_cost_competitiveness_id[0], cost_competitive)

    def test_supplier_relationship_strength_relation(self):
        # Test One2many relation for supplier relationship strength
        relationship_strength = self.env['scm.supplier_relationship_strength'].create({
            'supplier_id9': self.supplier.id,
            'relationship_score': 4.2,
            'comment': 'Strong partnership'
        })
        self.assertEqual(
            self.supplier.supplier_relationship_strength_id[0], relationship_strength)

    def test_supplier_rd_investment_relation(self):
        # Test One2many relation for supplier R&D investment
        rd_investment = self.env['scm.supplier_rd_investment'].create({
            'supplier_id7': self.supplier.id,
            'investment_amount': 50000,
            'description': 'New technology development'
        })
        self.assertEqual(
            self.supplier.supplier_rd_investment_id[0], rd_investment)

    def test_supplier_product_innovation_relation(self):
        # Test One2many relation for supplier product innovation
        product_innovation = self.env['scm.supplier_product_innovation'].create({
            'supplier_id8': self.supplier.id,
            'innovation_score': 4.8,
            'comment': 'Pioneered new materials'
        })
        self.assertEqual(
            self.supplier.supplier_product_innovation_id[0], product_innovation)

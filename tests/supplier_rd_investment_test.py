from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError
from datetime import date

class TestSupplierRDInvestment(TransactionCase):

    def setUp(self):
        super(TestSupplierRDInvestment, self).setUp()
        # Create a related supplier and research focus
        self.supplier = self.env['scm.supplier'].create({
            'name': 'Supplier B',
        })
        self.research_focus = self.env['scm.research_focus'].create({
            'name': 'Sustainability Focus',
        })
        # Set a company currency for testing
        self.currency = self.env.user.company_id.currency_id

    def test_rd_investment_creation(self):
        rd_investment = self.env['scm.supplier_rd_investment'].create({
            'supplier_id7': self.supplier.id,
            'amount_invested': 50000,
            'currency_id': self.currency.id,
            'investment_period_start': date(2024, 1, 1),
            'investment_period_end': date(2024, 12, 31),
            'investment_trend': 10.5,
            'research_focus': self.research_focus.id,
            'expected_roi': 20.0,
            'actual_roi': 18.0,
            'rd_collaboration': True,
            'environmental_impact': 'medium',
        })
        self.assertEqual(rd_investment.supplier_id7.id, self.supplier.id)
        self.assertEqual(rd_investment.amount_invested, 50000)
        self.assertEqual(rd_investment.currency_id.id, self.currency.id)
        self.assertEqual(rd_investment.research_focus.id, self.research_focus.id)
        self.assertTrue(rd_investment.rd_collaboration)

    def test_unique_supplier_investment_period_constraint(self):
        self.env['scm.supplier_rd_investment'].create({
            'supplier_id7': self.supplier.id,
            'amount_invested': 60000,
            'currency_id': self.currency.id,
            'investment_period_start': date(2024, 1, 1),
            'investment_period_end': date(2024, 12, 31),
        })
        with self.assertRaises(ValidationError):
            self.env['scm.supplier_rd_investment'].create({
                'supplier_id7': self.supplier.id,
                'amount_invested': 70000,  # Same supplier and investment period
                'currency_id': self.currency.id,
                'investment_period_start': date(2024, 1, 1),
                'investment_period_end': date(2024, 12, 31),
            })

    def test_investment_period_validation(self):
        # Check that the period start date must be before the end date
        with self.assertRaises(ValidationError):
            self.env['scm.supplier_rd_investment'].create({
                'supplier_id7': self.supplier.id,
                'amount_invested': 80000,
                'currency_id': self.currency.id,
                'investment_period_start': date(2024, 12, 31),
                'investment_period_end': date(2024, 1, 1),  # End date is before start date
            })

    def test_currency_default(self):
        rd_investment = self.env['scm.supplier_rd_investment'].create({
            'supplier_id7': self.supplier.id,
            'amount_invested': 90000,
            'investment_period_start': date(2024, 1, 1),
            'investment_period_end': date(2024, 12, 31),
        })
        self.assertEqual(rd_investment.currency_id.id, self.currency.id)  # Default currency of the company

    def test_expected_and_actual_roi(self):
        rd_investment = self.env['scm.supplier_rd_investment'].create({
            'supplier_id7': self.supplier.id,
            'amount_invested': 95000,
            'currency_id': self.currency.id,
            'investment_period_start': date(2024, 1, 1),
            'investment_period_end': date(2024, 12, 31),
            'expected_roi': 25.0,
            'actual_roi': 22.0,
        })
        self.assertEqual(rd_investment.expected_roi, 25.0)
        self.assertEqual(rd_investment.actual_roi, 22.0)

    def test_rd_collaboration(self):
        # Test that collaboration with external entities can be correctly recorded
        rd_investment = self.env['scm.supplier_rd_investment'].create({
            'supplier_id7': self.supplier.id,
            'amount_invested': 100000,
            'currency_id': self.currency.id,
            'investment_period_start': date(2024, 1, 1),
            'investment_period_end': date(2024, 12, 31),
            'rd_collaboration': True,
        })
        self.assertTrue(rd_investment.rd_collaboration)

    def test_environmental_impact(self):
        # Test different environmental impact levels
        rd_investment = self.env['scm.supplier_rd_investment'].create({
            'supplier_id7': self.supplier.id,
            'amount_invested': 120000,
            'currency_id': self.currency.id,
            'investment_period_start': date(2024, 1, 1),
            'investment_period_end': date(2024, 12, 31),
            'environmental_impact': 'high',
        })
        self.assertEqual(rd_investment.environmental_impact, 'high')


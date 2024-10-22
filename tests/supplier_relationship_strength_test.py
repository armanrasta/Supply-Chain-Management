from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError
from datetime import date


class TestSupplierRelationshipStrength(TransactionCase):

    def setUp(self):
        super(TestSupplierRelationshipStrength, self).setUp()
        self.supplier = self.env['scm.supplier'].create({
            'name': 'Test Supplier',
            'contact_email': 'test@supplier.com',
            'contact_phone': '123456789',
            'address': '123 Supplier Lane',
            'performance_score': 3.5,
        })

    def test_create_relationship_strength(self):
        # Test creating a SupplierRelationshipStrength record with valid data
        relationship_strength = self.env['scm.supplier_relationship_strength'].create({
            'supplier_id9': self.supplier.id,
            'relationship_start_date': '2004-01-07',
            'relationship_end_date': '2024-10-21',
            'communication_quality': 'good',
            'communication_frequency': 'regular',
            'trust_level': 'medium',
            'transparency_level': 'high',
            'collaboration_level': 'low',
            'issue_resolution_timing': 'fast',
            'on_time_delivery_rate': 33.33,
            'quality_compliance_rate': 66.66,
        })

        self.assertEqual(relationship_strength.supplier_id9, self.supplier)
        self.assertEqual(relationship_strength.communication_quality, 'good')
        self.assertEqual(relationship_strength.on_time_delivery_rate, 33.33)
        self.assertEqual(relationship_strength.quality_compliance_rate, 66.66)

    def test_missing_required_fields(self):
        # Test that creating a record without required fields raises ValidationError
        with self.assertRaises(ValidationError):
            self.env['scm.supplier_relationship_strength'].create({
                'communication_quality': 'good',  # Missing required supplier_id9
            })

    def test_relationship_score_computation(self):
        # Create a relationship record and test the computed relationship score
        relationship_strength = self.env['scm.supplier_relationship_strength'].create({
            'supplier_id9': self.supplier.id,
            'communication_quality': 'excellent',
            'communication_frequency': 'frequent',
            'trust_level': 'high',
            'transparency_level': 'high',
            'collaboration_level': 'high',
            'on_time_delivery_rate': 90.0,
            'quality_compliance_rate': 85.0,
        })

        # Compute the relationship score and check correctness
        relationship_strength._compute_relationship_score()

        expected_score = (4 + 3 + 3 + 3) / 4 + 0.9 + \
            0.85  # Formula in the model
        self.assertAlmostEqual(
            relationship_strength.relationship_score, expected_score)

    def test_invalid_dates(self):
        # Test validation errors for invalid dates
        with self.assertRaises(ValidationError):
            self.env['scm.supplier_relationship_strength'].create({
                'supplier_id9': self.supplier.id,
                'relationship_start_date': date(2024, 10, 21),
                # End date before start date
                'relationship_end_date': date(2004, 1, 7),
            })

    def test_unique_supplier_constraint(self):
        # Test the unique constraint on supplier relationship records
        self.env['scm.supplier_relationship_strength'].create({
            'supplier_id9': self.supplier.id,
            'communication_quality': 'good',
            'communication_frequency': 'regular',
            'trust_level': 'medium',
            'transparency_level': 'medium',
            'collaboration_level': 'medium',
            'on_time_delivery_rate': 92.0,
            'quality_compliance_rate': 90.0,
        })

        with self.assertRaises(ValidationError):
            self.env['scm.supplier_relationship_strength'].create({
                'supplier_id9': self.supplier.id,  # Duplicating supplier relationship
                'communication_quality': 'poor',
            })

    def test_invalid_delivery_rate(self):
        # Test that the on_time_delivery_rate field raises an error if invalid
        with self.assertRaises(ValidationError):
            self.env['scm.supplier_relationship_strength'].create({
                'supplier_id9': self.supplier.id,
                'on_time_delivery_rate': 150.0,  # Invalid rate (>100)
            })

        with self.assertRaises(ValidationError):
            self.env['scm.supplier_relationship_strength'].create({
                'supplier_id9': self.supplier.id,
                'on_time_delivery_rate': -10.0,  # Invalid rate (<0)
            })

    def test_invalid_quality_compliance_rate(self):
        # Test that the quality_compliance_rate field raises an error if invalid
        with self.assertRaises(ValidationError):
            self.env['scm.supplier_relationship_strength'].create({
                'supplier_id9': self.supplier.id,
                'quality_compliance_rate': 105.0,  # Invalid rate (>100)
            })

        with self.assertRaises(ValidationError):
            self.env['scm.supplier_relationship_strength'].create({
                'supplier_id9': self.supplier.id,
                'quality_compliance_rate': -5.0,  # Invalid rate (<0)
            })

    def test_ondelete_cascade(self):
        # Test the cascading delete behavior
        relationship_strength = self.env['scm.supplier_relationship_strength'].create({
            'supplier_id9': self.supplier.id,
            'communication_quality': 'good',
        })

        # Delete supplier and ensure relationship_strength is deleted
        self.supplier.unlink()
        self.assertFalse(self.env['scm.supplier_relationship_strength'].search(
            [('id', '=', relationship_strength.id)]))

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class SupplierRelationshipStrength(models.Model):
    _name = 'scm.supplier_relationship_strength'
    _description = 'Supplier Relationship Strength'

    supplier_id9 = fields.Many2one(
        'scm.supplier', string='Supplier', ondelete='cascade', required=True)
    relationship_start_date = fields.Date(
        string='Relationship Start Date', help='The date when the supplier relationship started.')
    relationship_end_date = fields.Date(
        string='Relationship End Date', help='The date when the supplier relationship ended, if applicable.')

    # Communication Effectiveness
    communication_quality = fields.Selection([
        ('poor', 'Poor'),
        ('average', 'Average'),
        ('good', 'Good'),
        ('excellent', 'Excellent')
    ],  string='Communication Quality',
        help='Overall quality of communication with the supplier.')

    communication_frequency = fields.Selection([
        ('rare', 'Rare'),
        ('occasional', 'Occasional'),
        ('regular', 'Regular'),
        ('frequent', 'Frequent')
    ],  string='Communication Frequency',
        help='Frequency of communication with the supplier.')

    # Trust and Transparency Levels
    trust_level = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High')
    ],  string='Trust Level',
        help='Level of trust in the supplier.')

    transparency_level = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High')
    ],  string='Transparency Level',
        help='Degree of transparency in supplier communications and dealings.')

    # Collaboration & Issue Resolution
    collaboration_level = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High')
    ],  string='Collaboration Level',
        help='Degree of collaboration with the supplier on joint projects, innovations, or problem-solving.')

    issue_resolution_timing = fields.Selection([
        ('slow', 'Slow'),
        ('average', 'Average'),
        ('fast', 'Fast')
    ],  string='Issue Resolution Timing',
        help='The speed at which issues are resolved with the supplier.')

    # Performance and Dependability
    on_time_delivery_rate = fields.Float(string='On-Time Delivery Rate (%)',
                                         help='Percentage of deliveries from the supplier that are on time.')
    quality_compliance_rate = fields.Float(string='Quality Compliance Rate (%)',
                                           help='Percentage of products or services provided by the supplier that meet agreed quality standards.')

    # Relationship Score (Composite Field)
    relationship_score = fields.Float(string='Overall Relationship Score',
                                      compute='_compute_relationship_score',
                                      store=True, help='Calculated score indicating the overall strength of the supplier relationship.')

    _sql_constraints = [
        ('unique_supplier_relationship', 'UNIQUE(supplier_id9)',
         'There can only be one active relationship strength record per supplier.')
    ]

    @api.depends('communication_quality', 'trust_level', 'transparency_level', 'collaboration_level', 'on_time_delivery_rate', 'quality_compliance_rate')
    def _compute_relationship_score(self):
        for record in self:
            # Example calculation for an overall relationship score
            communication_score = {'poor': 1, 'average': 2, 'good': 3, 'excellent': 4}.get(
                record.communication_quality, 0)
            trust_score = {'low': 1, 'medium': 2,
                           'high': 3}.get(record.trust_level, 0)
            transparency_score = {'low': 1, 'medium': 2,
                                  'high': 3}.get(record.transparency_level, 0)
            collaboration_score = {'low': 1, 'medium': 2, 'high': 3}.get(
                record.collaboration_level, 0)
            delivery_score = record.on_time_delivery_rate / 100  # Normalize to a 0-1 scale
            quality_score = record.quality_compliance_rate / 100  # Normalize to a 0-1 scale

            # Final relationship score calculation (could be adjusted as needed)
            record.relationship_score = (communication_score + trust_score + transparency_score +
                                         collaboration_score) / 4 + delivery_score + quality_score

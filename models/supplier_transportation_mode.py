from odoo import models, fields


class TransportationMode(models.Model):
    _name = 'scm.transportation_mode'
    _description = 'Transportation Mode Availability'

    name = fields.Char(string='Mode Name', required=True)
    availability_probability = fields.Float(
        string='Availability Probability (%)', default=100.0, help='Probability that this mode is available for use.')
    description = fields.Text(string='Description')
    active = fields.Boolean(string='Active', default=True)
    network_robustness_id = fields.Many2many(
        'scm.network_robustness',
        'network_robustness_transportation_rel',  # custom relation table
        'transportation_mode_id',  # second column name (related model side)
        'network_robustness_id',  # first column name (self side)
        string='Network Robustness Parameters')

    _sql_constraints = [
        ('unique_transport_mode', 'UNIQUE(name)',
         'Each transportation mode must have a unique name.')
    ]

from odoo import models, fields


class Serial(models.Model):
    _name = 'scm.serial'
    _description = 'Serial Number Information'

    name = fields.Char(string='Serial Number', required=True)
    serial_inventory_item_id = fields.Many2one(
        'scm.inventory_item', string='Inventory Item', ondelete='cascade')
    status = fields.Selection([
        ('available', 'Available'),
        ('reserved', 'Reserved'),
        ('sold', 'Sold'),
        ('returned', 'Returned'),
    ], string='Status', default='available')

    _sql_constraints = [
        ('name_uniq', 'unique(name)', "Serial Number must be unique!"),
    ]

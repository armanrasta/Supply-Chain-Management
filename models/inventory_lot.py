from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Lot(models.Model):
    _name = 'scm.lot'
    _description = 'Lot Information'

    name = fields.Char(string='Lot Number', required=True)
    lot_inventory_item_id = fields.Many2one(
        'scm.inventory_item', string='Inventory Item', ondelete='cascade')
    quantity = fields.Float(string='Quantity', default=0)
    manufacture_date = fields.Date(string='Manufacture Date')
    expiry_date = fields.Date(string='Expiry Date')

    @api.constrains('quantity')
    def _check_quantity(self):
        for lot in self:
            if lot.quantity < 0:
                raise ValidationError("Lot quantity cannot be negative.")

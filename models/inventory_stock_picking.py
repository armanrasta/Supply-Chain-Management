from odoo import models, fields, api


class StockPicking(models.Model):

    _inherit = 'stock.picking'

    def _assign_serial_or_lot(self):
        res = super(StockPicking, self)._assign_serial_or_lot()
        for move in self.move_lines:
            if move.product_id.tracking in ['lot', 'serial'] and move.product_id.expiry_date:
                quants = move.quant_id.filtered(
                    lambda q: q.lot_id and q.lot_id.expiry_date)
                quants = quants.sorted(key=lambda q: q.lot_id.expiry_date)
                move.quant_id = quants
        return res

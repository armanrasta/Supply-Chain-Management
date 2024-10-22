from odoo import models, fields


class SupplierContactPerson(models.Model):
    _name = 'scm.supplier_contact_person'
    _description = 'Supplier Contact Person'

    name = fields.Char(string='Contact Name', required=True)
    email = fields.Char(string='Email')
    phone = fields.Char(string='Phone')
    position = fields.Char(string='Position')
    supplier_id1 = fields.Many2one('scm.supplier', string='Supplier', ondelete='cascade')

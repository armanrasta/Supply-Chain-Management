from odoo import models, fields, api
from odoo.exceptions import ValidationError


class InventoryItemCategory(models.Model):
    _name = 'scm.inventory_item_category'
    _description = 'Inventory Item Category'
    _parent_name = "parent_id"
    _parent_store = True
    _rec_name = 'complete_name'
    _order = 'complete_name'

    name = fields.Char(string='Category Name', required=True)
    complete_name = fields.Char(
        string='Complete Name', compute='_compute_complete_name', store=True)
    is_subcategory = fields.Boolean(string='Is Sub-Category')
    parent_id = fields.Many2one('scm.inventory_item_category', 'Parent Category', ondelete='restrict', domain="[('is_subcategory', '=', False)]")
    parent_path = fields.Char(index=True)
    child_id = fields.One2many('scm.inventory_item_category', 'parent_id', string='Sub-Categories')
    item_id = fields.One2many('scm.inventory_item', 'category_id', string='Inventory Items')
    holding_cost = fields.Float(
        string='Holding Cost', help='Holding cost per unit for this category')

    @api.depends('name', 'parent_id.complete_name')
    def _compute_complete_name(self):
        for category in self:
            if category.parent_id:
                category.complete_name = '%s / %s' % (
                    category.parent_id.complete_name, category.name)
            else:
                category.complete_name = category.name

    @api.constrains('is_subcategory', 'parent_id')
    def _check_subcategory(self):
        for category in self:
            if category.is_subcategory and not category.parent_id:
                raise ValidationError(
                    'Sub-categories must have a parent category.')
            if not category.is_subcategory and category.parent_id:
                raise ValidationError(
                    'A category marked as a main category cannot have a parent.')

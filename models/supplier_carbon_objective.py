from odoo import models, fields, api
from odoo.exceptions import ValidationError


class CarbonObjective(models.Model):
    _name = 'scm.carbon_objective'
    _description = 'Carbon Footprint Reduction Objective'

    name = fields.Char(string='Objective Name', required=True)
    description = fields.Text(string='Description')
    target_reduction = fields.Float(string='Target Reduction (%)', required=True, help='Percentage reduction target.')
    start_date = fields.Date(string='Start Date', required=True, default=fields.Date.today)
    end_date = fields.Date(string='End Date', required=True)
    current_progress = fields.Float(string='Current Progress (%)', compute='_compute_current_progress', store=True, readonly=True)
    supplier_id4 = fields.Many2many(
        comodel_name='scm.supplier',
        relation='supplier_carbon_relation',
        column1='carbon_objective_id',
        column2='supplier_id4',
        string='Related Suppliers'
    )
    inventory_item_id4 = fields.Many2many(
        'scm.inventory_item',
        'carbon_objective_inventory_rel',
        'carbon_objective_id',
        'inventory_item_id4',  # Make sure this matches exactly
        string='Related Inventory Items'
    )
    facility_ids = fields.Many2many(
        'scm.warehouse_location', 
        'carbon_objective_facility_rel',  # **Ensure this table is unique if still needed**
        'carbon_objective_id',            # First column name (self side)
        'facility_id',                    # Second column name (related model side)
        string='Related Facilities'
    )
    active = fields.Boolean(string='Active', default=True)

    # @api.depends('target_reduction', 'inventory_item_id', 'supplier_id4', 'facility_id')
    # def _compute_current_progress(self):
    #     for record in self:
    #         pass

    @api.constrains('end_date', 'start_date')
    def _check_dates(self):
        for record in self:
            if record.end_date < record.start_date:
                raise ValidationError('End date must be after the start date.')

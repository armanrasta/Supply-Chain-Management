from odoo import models, fields, api


class WarehouseLocation(models.Model):
    _name = 'scm.warehouse_location'
    _description = 'Warehouse Location'
    _parent_name = "parent_location_id"
    _parent_store = True
    _rec_name = 'complete_name'
    _order = 'complete_name'

    name = fields.Char(string='Location Name', required=True)
    complete_name = fields.Char(
        string='Complete Name', compute='_compute_complete_name', store=True, recursive=True)
    capacity = fields.Float(string='Storage Capacity',
                            help="Storage capacity in cubic meters")
    utilization = fields.Float(
        string='Utilization (%)', compute='_compute_utilization')
    address = fields.Text(string='Address', required=True)
    fixed_costs = fields.Float(
        string='Fixed Costs', default=0.0, help='Monthly fixed costs for the facility.')
    active = fields.Boolean(string='Active', default=True)
    
    currency_id = fields.Many2one('res.currency', string='Currency',
                                  default=lambda self: self.env.user.company_id.currency_id.id)
    warehouse_id = fields.Many2one(
        'stock.warehouse', string='Warehouse', required=True)
    parent_location_id = fields.Many2one(
        'scm.warehouse_location', string='Parent Location', ondelete='cascade')
    parent_path = fields.Char(index=True)
    child_location_id = fields.One2many(
        'scm.warehouse_location', 'parent_location_id', string='Child Locations')
    w_inventory_item_id = fields.One2many(
        'scm.inventory_item', 'location_id', string='Inventory Items')
    carbon_objective_ids = fields.Many2many(
        'scm.carbon_objective',        # **Corrected related model**
        'warehouse_carbon_rel',        # **Unique relation table**
        'warehouse_id',                # **First column (self side)**
        'carbon_objective_id',         # **Second column (related model side)**
        string='Carbon Objectives'
    )

    _sql_constraints = [
        ('unique_location_name', 'UNIQUE(name)',
         'Each warehouse location must have a unique name.')
    ]

    @api.depends('name', 'parent_location_id.complete_name')
    def _compute_complete_name(self):
        for location in self:
            if location.parent_location_id:
                location.complete_name = '%s / %s' % (
                    location.parent_location_id.complete_name, location.name)
            else:
                location.complete_name = location.name

    @api.depends('capacity', 'w_inventory_item_id')
    def _compute_utilization(self):
        for location in self:
            total_volume = sum(
                item.volume * item.stock_level for item in location.w_inventory_item_id)
            location.utilization = (
                total_volume / location.capacity * 100) if location.capacity else 0

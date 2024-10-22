from odoo import models, fields, api
from datetime import timedelta
from math import sqrt
from odoo.exceptions import ValidationError


class InventoryItem(models.Model):
    _name = 'scm.inventory_item'
    _description = 'Inventory Item'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Item Name', required=True )
    description = fields.Text(string='Description')
    stock_level = fields.Float(string='Stock Level', default=0 )
    reorder_point = fields.Float(
        string='Reorder Point', compute='_compute_reorder_point', store=True)
    safety_stock = fields.Float(
        string='Safety Stock', compute='_compute_safety_stock', store=True)
    lead_time_days = fields.Integer(string='Lead Time (Days)', default=0)
    unit_cost = fields.Float(string='Unit Cost', digits=(10, 2) )
    last_order_date = fields.Date(string='Last Order Date')
    expiry_date = fields.Date(string='Expiry Date')

    needs_reorder = fields.Boolean(
        string='Needs Reorder', compute='_compute_needs_reorder', store=True)
    total_cost = fields.Float(
        string='Total Cost', compute='_compute_total_cost', store=True)
    volume = fields.Float(string='Volume', help="Volume in cubic meters")
    weight = fields.Float(string='Weight', help="Weight in kilograms")
    image = fields.Binary(string="Item Image")

    demand_volatility = fields.Float(string='Demand Volatility',
                                     help='Measure of demand fluctuation', default=0.0)
    lead_time_variability = fields.Float(string='Lead Time Variability',
                                         help='Standard deviation of lead time', default=0.0)
    turnover_ratio_sku = fields.Float(string='Turnover Ratio (SKU)',
                                      compute='_compute_turnover_ratio_sku', store=True)
    turnover_ratio_category = fields.Float(string='Turnover Ratio (Category)',
                                           compute='_compute_turnover_ratio_category', store=True)
    cost_method = fields.Selection([('fifo', 'First In First Out (FIFO)'), ('lifo', 'Last In First Out (LIFO)'), (
        'average', 'Average Cost')], string='Costing Method', default='average' )
    tracking = fields.Selection([('none', 'No Tracking'), ('serial', 'By Serial Number'), (
        'lot', 'By Lot Number'),], string='Tracking', default='none' )

    abc_class = fields.Selection([
        ('A', 'A - High Value'),
        ('B', 'B - Moderate Value'),
        ('C', 'C - Low Value')
    ], string='ABC Classification', default='C', compute='_compute_abc_class', store=True)
    carbon_objective_id = fields.Many2many(
        'scm.carbon_objective',
        'carbon_objective_inventory_rel',
        'inventory_item_id4',
        'carbon_objective_id',
        string='Carbon Objectives',
        ondelete='restrict',
    )
    network_robustness_id = fields.Many2many(
        'scm.network_robustness',
        'network_robustness_inventory_rel',  # custom relation table
        'inventory_item_id3',  # second column name
        'network_robustness_id',  # first column name
        string='Network Robustness Parameters')

    uom_id = fields.Many2one('uom.uom', string='Unit of Measure', required=True,
                             default=lambda self: self.env.ref('uom.product_uom_unit').id)
    stock_quant_id = fields.Many2many('stock.quant', string='Stock Quants')
    # product_id = fields.Many2one('product.product', string='Product', ondelete='cascade')
    lot_id = fields.One2many('scm.lot', 'lot_inventory_item_id', string='Lots')
    serial_id = fields.One2many(
        'scm.serial', 'serial_inventory_item_id', string='Serial Numbers')
    location_id = fields.Many2one(
        'scm.warehouse_location', string='Warehouse Location', ondelete='set null' )
    category_id = fields.Many2one(
        'scm.inventory_item_category', string='Category', ondelete='restrict')
    supplier_id13 = fields.Many2many(
        'scm.supplier',
        # 'inventory_supplier_relation',
        # 'supplier_id13',
        # 'carbon_objective_id',
        string='Supplier',
        ondelete='restrict'
    )

    # @api.model
    # def create(self, vals):
    #     product = self.env['product.product'].create({
    #         'name': vals.get('name'),
    #         'type': 'product',
    #         'list_price': vals.get('unit_cost'),
    #         'standard_price': vals.get('unit_cost'),
    #     })
    #     vals['product_id'] = product.id
    #     return super(InventoryItem, self).create(vals)

    # def write(self, vals):
    #     if 'unit_cost' in vals:
    #         self.product_id.write({
    #             'list_price': vals['unit_cost'],
    #             'standard_price': vals['unit_cost'],
    #         })
    #     return super(InventoryItem, self).write(vals)

    @api.model
    def check_reorder_levels(self):
        # Find items that need reordering
        items_to_reorder = self.search([
            ('stock_level', '<=', fields.Float.sum(
                ['reorder_point', 'safety_stock'])),
            ('supplier_id13', '!=', False),
            ('needs_reorder', '=', True),
        ])

        # Group items by supplier to create consolidated purchase orders
        supplier_items = {}
        for item in items_to_reorder:
            if item.supplier_id13 not in supplier_items:
                supplier_items[item.supplier_id13] = []
            supplier_items[item.supplier_id13].append(item)

        purchase_order_obj = self.env['purchase.order']
        for supplier, items in supplier_items.items():
            # Create a new purchase order for each supplier
            order_lines = []
            for item in items:
                quantity_to_order = max(
                    item.reorder_point - item.stock_level + item.safety_stock, 0)
                if quantity_to_order > 0:
                    order_lines.append((0, 0, {
                        'product_id': item.product_id.id,
                        'name': item.name,
                        'product_qty': quantity_to_order,
                        'price_unit': item.unit_cost,
                        'date_planned': fields.Datetime.now() + timedelta(days=item.lead_time_days),
                    }))

            if order_lines:
                purchase_order = purchase_order_obj.create({
                    'partner_id': supplier.id,
                    'order_line': order_lines,
                })

                # Update last_order_date for all items in this order
                items.write({'last_order_date': fields.Date.today()})

                # Send email notification
                template = self.env.ref(
                    'scm.email_template_purchase_order_created', raise_if_not_found=False)
                if template:
                    template.send_mail(purchase_order.id, force_send=True)

        return True

    def adjust_stock(self, qty, location_id=None, lot_id=None, serial_id=None):
        self.ensure_one()
        if qty == 0:
            raise ValidationError("Quantity must be non-zero.")

        if self.tracking == 'serial' and abs(qty) > 1:
            raise ValidationError(
                "For items tracked by serial numbers, quantity must be 1 or -1.")

        self.stock_level += qty

        quant_vals = {
            'product_id': self.product_id.id,
            'location_id': location_id or self.env.ref('stock.stock_location_stock').id,
            'quantity': qty,
            'lot_id': lot_id,
            'owner_id': False,
            'inventory_item_id': self.id,
        }
        if self.tracking == 'serial' and serial_id:
            quant_vals['serial_number_id'] = serial_id
        elif self.tracking == 'lot' and not lot_id:
            raise ValidationError(
                "Lot number is required for lot-tracked items.")

        self.env['stock.quant'].create(quant_vals)

        # Update the cost based on the costing method
        if qty > 0:  # Incoming stock
            if self.cost_method in ['fifo', 'lifo']:
                self.stock_quant_id.create({
                    'product_id': self.product_id.id,
                    'inventory_item_id': self.id,
                    'quantity': qty,
                    'cost': self.unit_cost,
                    'in_date': fields.Datetime.now(),
                })
            elif self.cost_method == 'average':
                total_qty = self.stock_level
                total_value = self.total_cost + (qty * self.unit_cost)
                self.unit_cost = total_value / total_qty if total_qty else 0

    def rebalance_inventory(self):
        for item in self:
            # Fetch demand forecast
            forecast = self.env['scm.demand_forecast'].search([
                ('inventory_item_id', '=', item.id),
                ('scenario', '=', 'most_likely'),
                ('period_start_date', '<=', fields.Date.today()),
                ('period_end_date', '>=', fields.Date.today()),
            ], limit=1)
            if forecast:
                required_stock = forecast.forecasted_quantity + item.safety_stock
                current_stock = item.stock_level
                if current_stock < required_stock:
                    deficit = required_stock - current_stock
                    # Find locations with excess stock
                    excess_items = self.search([
                        ('product_id', '=', item.product_id.id),
                        ('stock_level', '>',
                         forecast.forecasted_quantity + item.safety_stock),
                    ])
                    for excess_item in excess_items:
                        transferable_qty = excess_item.stock_level - \
                            (forecast.forecasted_quantity + item.safety_stock)
                        transfer_qty = min(deficit, transferable_qty)
                        if transfer_qty > 0:
                            excess_item.transfer_stock(
                                item.location_id.id, transfer_qty)
                            deficit -= transfer_qty
                            if deficit <= 0:
                                break

    # Computes
    @api.depends('demand_volatility', 'lead_time_days', 'lead_time_variability')
    def _compute_reorder_point(self):
        Z = 1.65  # For 95% service level; adjust as needed
        for record in self:
            # Assuming demand_volatility represents average demand
            average_demand = record.demand_volatility
            lead_time = record.lead_time_days
            variability = record.lead_time_variability
            record.reorder_point = (
                average_demand * lead_time) + (Z * record.demand_volatility * sqrt(variability))

    @api.depends('stock_level', 'unit_cost', 'cost_method', 'stock_quant_id')
    def _compute_total_cost(self):
        for record in self:
            if record.cost_method == 'fifo':
                record.total_cost = sum(
                    quant.quantity * quant.cost for quant in record.stock_quant_id.sorted(key=lambda r: r.in_date))
            elif record.cost_method == 'lifo':
                record.total_cost = sum(
                    quant.quantity * quant.cost for quant in record.stock_quant_id.sorted(key=lambda r: r.in_date, reverse=True))
            elif record.cost_method == 'average':
                record.total_cost = record.stock_level * record.unit_cost

    @api.depends('stock_level', 'reorder_point', 'safety_stock')
    def _compute_needs_reorder(self):
        for record in self:
            record.needs_reorder = record.stock_level <= (
                record.reorder_point + record.safety_stock)

    @api.depends('demand_volatility', 'lead_time_days')
    def _compute_safety_stock(self):
        Z = 1.65  # For 95% service level
        for record in self:
            sigma_demand = record.demand_volatility
            lead_time = record.lead_time_days
            record.safety_stock = Z * sigma_demand * sqrt(lead_time)

    # @api.depends('total_cost', 'stock_level', 'sale_order_line_id')
    # def _compute_abc_class(self): # Needs classification in views with cron jobs
    #     for item in self:
    #         sales = self.env['sale.order.line'].search([('product_id', '=', item.product_id.id)])
    #         total_sales = sum(sales.mapped('product_uom_qty')) * item.unit_cost
    #         if total_sales > 100000:  # Thresholds can be dynamic or configurable
    #             item.abc_class = 'A'
    #         elif total_sales > 50000:
    #             item.abc_class = 'B'
    #         else:
    #             item.abc_class = 'C'

    @api.model
    def notify_upcoming_expirations(self):
        threshold_days = 30  # Notify items expiring within 30 days
        today = fields.Date.today()
        threshold_date = today + timedelta(days=threshold_days)
        lots = self.env['scm.lot'].search([
            ('expiry_date', '<=', threshold_date),
            ('expiry_date', '>=', today),
        ])
        for lot in lots:
            template = self.env.ref(
                'scm.email_template_expiry_notification', raise_if_not_found=False)
            if template:
                template.send_mail(lot.id, force_send=True)

    # @api.depends('stock_level', 'sale_order_line_id')
    # def _compute_turnover_ratio_sku(self):
    #     for item in self:
    #         sales = self.env['sale.order.line'].search([('product_id', '=', item.product_id.id)])
    #         total_sales = sum(sales.mapped('product_uom_qty'))
    #         inventory = item.stock_level
    #         item.turnover_ratio_sku = total_sales / (inventory + 1)  # Prevent division by zero

    # @api.depends('category_id', 'sale_order_line_id', 'category_id.item_id.stock_level')
    # def _compute_turnover_ratio_category(self):
    #     for item in self:
    #         category = item.category_id
    #         sales = self.env['sale.order.line'].search([('product_id.category_id', '=', category.id)])
    #         total_sales = sum(sales.mapped('product_uom_qty'))
    #         inventory = sum(category.item_id.mapped('stock_level'))
    #         item.turnover_ratio_category = total_sales / (inventory + 1) # Prevent division by zero

    # def generate_regional_forecasts(self):
    #     for item in self:
    #         regions = self.env['res.country.state'].search([])
    #         for region in regions:
    #             # Example logic: Modify forecast based on regional factors
    #             base_forecast = self.env['scm.demand_forecast'].search([
    #                 ('inventory_item_id', '=', item.id),
    #                 ('region_id', '=', region.id),
    #                 ('scenario', '=', 'most_likely'),
    #             ], limit=1)
    #             if base_forecast:
    #                 # Adjust forecast based on regional demand variation
    #                 base_forecast.forecasted_quantity *= region.demand_multiplier

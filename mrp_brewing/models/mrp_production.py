# Part of Open Architechts Consulting sprl. See LICENSE file for full
# copyright and licensing details.

from odoo import api, fields, models


class MrpProduction(models.Model):
    """ Manufacturing Orders """

    _inherit = "mrp.production"

    _order = "date_planned_start desc"  # initially "date_planned_start asc,id"

    lot_ids = fields.Many2many(
        string="Finished Product Lot",
        comodel_name="stock.production.lot",
        compute="_compute_lot_ids",
        help="Lots of produced product.",
    )
    brew_number = fields.Char(
        string="Brew Number", compute="_compute_brew_number", store=True
    )
    brew_order_name = fields.Char(
        compute="_compute_brew_order_name", string="Brew Order Name"
    )
    # actually a One2one relation
    brew_orders = fields.One2many(
        comodel_name="brew.order",
        inverse_name="production_order_id",
        string="Brew Order",
        readonly=True,
    )
    # todo remove master_mo_id and rely only on brew order as parent ?
    master_mo_id = fields.Many2one(
        comodel_name="mrp.production",
        string="Master MO",
        domain=[
            ("product_tmpl_id.is_brewable", "=", True),
            ("state", "not in", ["draft", "cancel"]),
        ],
    )
    child_mo_ids = fields.One2many(
        comodel_name="mrp.production",
        inverse_name="master_mo_id",
        string="Children production order",
    )

    @api.model
    def create(self, vals):
        """
        If no master_mo_id is provided, set the eldest MO as the master_mo_id.
        A parent MO is a Mo which is the "origin" of current MO.
        In the case of mrp_brewing, eldest MO is created by the
        brew order."""

        mo = super().create(vals)
        master_mo_id = vals.get("master_mo_id")

        if not master_mo_id:
            master_mo = parent_mo = self.search([("name", "=", mo.origin)], limit=1)
            while parent_mo:
                master_mo = parent_mo
                parent_mo = self.search([("name", "=", parent_mo.origin)], limit=1)

            master_mo_id = master_mo.id

        mo.master_mo_id = master_mo_id
        return mo

    @api.multi
    @api.depends(
        "master_mo_id",
        "master_mo_id.brew_number",
        "brew_orders.brew_number",
    )
    def _compute_brew_number(self):
        for mo in self:
            if mo.master_mo_id:
                mo.brew_number = mo.master_mo_id.brew_number
            else:
                # brew_orders is a one2one relation
                mo.brew_number = mo.brew_orders.brew_number

    @api.multi
    @api.depends(
        "master_mo_id",
        "master_mo_id.brew_number",
        "brew_orders.state",
        "brew_orders.brew_number",
        "brew_orders.start_date",
    )
    def _compute_brew_order_name(self):
        for mo in self:
            master_mo = mo.master_mo_id or mo
            if master_mo.brew_orders:
                mo.brew_order_name = master_mo.brew_orders[0].name
            else:
                mo.brew_order_name = "/"

    @api.multi
    @api.depends("finished_move_line_ids.lot_produced_id")
    def _compute_lot_ids(self):
        for mo in self:
            target_product_move_lines = mo.finished_move_line_ids.filtered(
                lambda sml: sml.product_id == mo.product_id
            )
            mo.lot_ids = target_product_move_lines.mapped("lot_id")

    @api.multi
    def name_get(self):
        res = []
        for record in self:
            if record.origin:
                name = "[{}] {}".format(record.origin, record.name)
            else:
                name = record.name
            res.append((record.id, name))
        return res

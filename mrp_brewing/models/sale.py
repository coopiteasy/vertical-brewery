# Copyright 2021 Coop IT Easy SCRL fs
#   Houssine Bakkali <houssine@coopiteasy.be>
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    # todo move to custom module
    @api.multi
    @api.onchange("pricelist_id")
    def onchange_price_list(self):
        if not self.pricelist_id:
            self.note = ""
        else:
            self.note = self.pricelist_id.particular_conditions

    # todo move to custom module
    @api.multi
    @api.onchange("partner_id")
    def onchange_partner_id(self):
        super(SaleOrder, self).onchange_partner_id()
        self.onchange_price_list()


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    product_lot_ids = fields.Many2many(
        "stock.production.lot",
        string="Stock Product Lot",
        compute="_compute_stock_product",
    )
    effective_date = fields.Date(
        related="order_id.effective_date", string="Effective Date"
    )

    @api.multi
    def _compute_stock_product(self):
        """Computes the delivered product lot on sale order lines, based on
        done stock moves related to its procurements
        """

        for so_line in self:
            moves = so_line.move_ids.filtered(lambda m: m.state == "done")
            move_line_ids = moves.mapped("move_line_ids")
            lots = move_line_ids.mapped("lot_id")
            so_line.product_lot_ids = lots

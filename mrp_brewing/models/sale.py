# Part of Open Architechts Consulting sprl. See LICENSE file for full
# copyright and licensing details.
from datetime import datetime, timedelta

from odoo import api, fields, models
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.multi
    def _get_commitment_date(self):
        """Compute the commitment date"""
        for order in self:
            dates_list = []
            order_datetime = datetime.strptime(
                order.date_order, DEFAULT_SERVER_DATE_FORMAT
            )
            for line in order.order_line:
                if line.state == "cancel":
                    continue
                dt = order_datetime + timedelta(days=line.customer_lead or 0.0)
                dt_s = dt.strftime(DEFAULT_SERVER_DATE_FORMAT)
                dates_list.append(dt_s)
            if dates_list:
                return min(dates_list)

    commitment_date = fields.Date(
        string="Commitment Date",
        default=_get_commitment_date,
        help="Date by which the products are sure to be delivered. This is a "
        "date that you can promise to the customer, based on the Product "
        "Lead Times.",
    )

    @api.multi
    @api.onchange("pricelist_id")
    def onchange_price_list(self):
        if not self.pricelist_id:
            self.note = ""
        else:
            self.note = self.pricelist_id.particular_conditions

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

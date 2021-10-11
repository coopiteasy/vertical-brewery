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

    # FIXME: cf. _compute_stock_product
    # product_lot_ids = fields.Many2many(
    #     "stock.production.lot",
    #     string="Stock Product Lot",
    #     compute="_compute_stock_product",
    # )
    effective_date = fields.Date(
        related="order_id.effective_date", string="Effective Date"
    )

    @api.multi
    def _compute_stock_product(self):
        """Computes the delivered product lot on sale order lines, based on
        done stock moves related to its procurements
        """

        # FIXME: in 11.0, `procurement` has been merged in `stock`
        # - model `procurement.order` doesn't exist anymore
        # - simply delete?
        # - could `move_ids` and `_compute_qty_delivered` be used instead?
        #   (https://github.com/OCA/OCB/blob/12.0/addons/sale_stock/models/sale_order.py#L186)  # noqa

        for line in self:
            product_lot_ids = []
            for move in line.procurement_ids.mapped("move_ids").filtered(
                lambda r: r.state == "done" and not r.scrapped
            ):
                if move.location_dest_id.usage == "customer" and len(move.lot_ids) > 0:
                    product_lot_ids.append(move.lot_ids.ids[0])
            line.product_lot_ids = product_lot_ids

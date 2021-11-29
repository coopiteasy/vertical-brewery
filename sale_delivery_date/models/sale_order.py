# Copyright 2021 Coop IT Easy SCRL fs
#   Robin Keunen
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    delivery_done_date = fields.Datetime(
        compute="_compute_delivery_info",
        string="Delivery done date",
        readonly=True,
    )
    delivery_status = fields.Selection(
        [
            ("to_deliver", "To deliver"),
            ("delivered", "Delivered"),
            ("cancelled", "Cancelled"),
        ],
        compute="_compute_delivery_info",
        string="Delivery status",
        search="_search_delivery_status",
        readonly=True,
    )

    @api.multi
    @api.depends(
        "state",
        "picking_ids",
        "picking_ids.state",
        "picking_ids.date_done",
        "picking_ids.date_stock_move",
    )
    def _compute_delivery_info(self):
        for sale_order in self:
            if sale_order.state not in ["sale", "done"]:
                sale_order.delivery_done_date = False
                sale_order.delivery_status = False
                continue

            all_pickings = sale_order.picking_ids
            if all_pickings and all(p.state == "cancel" for p in all_pickings):
                sale_order.delivery_done_date = False
                sale_order.delivery_status = "cancelled"
                continue

            pickings = all_pickings.filtered(
                lambda p: p.state not in ("draft", "cancel")
            )
            if not pickings:
                date_stock_move = None
                delivery_status = None
            elif all(p.state == "done" for p in pickings):
                date_stock_moves = [
                    p.date_stock_move for p in pickings if p.date_stock_move
                ]
                if date_stock_moves:
                    date_stock_move = max(date_stock_moves)
                else:
                    date_stock_move = max(p.date_done for p in pickings)
                delivery_status = "delivered"
            else:
                date_stock_move = None
                delivery_status = "to_deliver"

            sale_order.delivery_done_date = date_stock_move
            sale_order.delivery_status = delivery_status

    def _search_delivery_status(self, operator, value):
        filter_function = {
            "=": lambda so: so.delivery_status == value,
            "!=": lambda so: so.delivery_status != value,
        }
        sale_orders = self.search([]).filtered(filter_function[operator])
        return [("id", "in", sale_orders.ids)]

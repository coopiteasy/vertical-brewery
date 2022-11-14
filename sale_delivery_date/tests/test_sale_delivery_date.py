# Copyright 2021 Coop IT Easy SC
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from datetime import timedelta

from odoo.fields import Datetime
from odoo.tests.common import TransactionCase


class TestStockPicking(TransactionCase):
    def setUp(self):
        super().setUp()
        self.partner = self.browse_ref("base.res_partner_1")
        self.product1 = self.browse_ref("product.product_product_25")
        self.stock_location = self.env.ref("stock.stock_location_stock")
        self.customer_location = self.env.ref("stock.stock_location_customers")
        self.uom_unit = self.browse_ref("uom.product_uom_unit")

    def _create_picking(self):
        picking = self.env["stock.picking"].create(
            {
                "picking_type_id": self.ref("stock.picking_type_out"),
                "location_id": self.stock_location.id,
                "location_dest_id": self.customer_location.id,
                "partner_id": self.partner.id,
            }
        )
        self.env["stock.move"].create(
            {
                "picking_id": picking.id,
                "product_id": self.product1.id,
                "name": self.product1.name,
                "product_uom": self.uom_unit.id,
                "location_id": self.stock_location.id,
                "location_dest_id": self.customer_location.id,
                "product_uom_qty": 1,
            }
        )
        return picking

    def _create_sale_order(
        self,
    ):
        sale_order = self.env["sale.order"].create(
            {
                "partner_id": self.partner.id,
            }
        )

        self.env["sale.order.line"].create(
            {
                "order_id": sale_order.id,
                "product_id": self.product1.id,
                "price_unit": 100,
                "product_uom_qty": 1,
            }
        )
        return sale_order

    def test_stock_move_date_set_to_date_stock_move(self):
        picking = self._create_picking()
        picking.date_stock_move = Datetime.now() - timedelta(days=3)
        picking.action_confirm()
        move = picking.move_lines  # only one move in the picking
        move.quantity_done = 1
        picking.action_done()
        self.assertEqual(move.date, picking.date_stock_move)

    def test_stock_move_date_set_to_date_done(self):
        picking = self._create_picking()
        picking.action_confirm()
        move = picking.move_lines  # only one move in the picking
        move.quantity_done = 1
        picking.action_done()
        self.assertEqual(move.date, picking.date_done)

    def test_delivery_status_date_done(self):
        sale_order = self._create_sale_order()
        self.assertFalse(sale_order.delivery_status)
        self.assertFalse(sale_order.delivery_done_date)

        sale_order.action_confirm()
        self.assertEqual(sale_order.delivery_status, "to_deliver")
        self.assertFalse(sale_order.delivery_done_date)

        picking = sale_order.picking_ids  # only one picking for the sale order
        picking.action_confirm()
        move = picking.move_lines  # only one move in the picking
        move.quantity_done = 1
        picking.action_done()
        self.assertEqual(sale_order.delivery_status, "delivered")
        self.assertEqual(sale_order.delivery_done_date, picking.date_done)

    def test_delivery_status_date_stock_move(self):
        sale_order = self._create_sale_order()
        self.assertFalse(sale_order.delivery_status)
        self.assertFalse(sale_order.delivery_done_date)

        sale_order.action_confirm()
        self.assertEqual(sale_order.delivery_status, "to_deliver")
        self.assertFalse(sale_order.delivery_done_date)

        picking = sale_order.picking_ids  # only one picking for the sale order
        picking.action_confirm()
        date_stock_move = Datetime.now() - timedelta(days=3)
        picking.date_stock_move = date_stock_move
        move = picking.move_lines  # only one move in the picking
        move.quantity_done = 1
        picking.action_done()
        self.assertEqual(sale_order.delivery_status, "delivered")
        self.assertEqual(sale_order.delivery_done_date, date_stock_move)

# Copyright 2021 Coop IT Easy SCRL fs
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.fields import Datetime
from odoo.tests.common import TransactionCase


class TestStockPicking(TransactionCase):
    def setUp(self):
        super().setUp()
        partner = self.browse_ref("base.res_partner_1")
        product1 = self.browse_ref("product.product_product_25")
        stock_location = self.env.ref("stock.stock_location_stock")
        customer_location = self.env.ref("stock.stock_location_customers")
        uom_unit = self.browse_ref("uom.product_uom_unit")

        self.picking = self.env["stock.picking"].create(
            {
                "picking_type_id": self.ref("stock.picking_type_out"),
                "location_id": stock_location.id,
                "location_dest_id": customer_location.id,
                "partner_id": partner.id,
            }
        )
        self.move = self.env["stock.move"].create(
            {
                "picking_id": self.picking.id,
                "product_id": product1.id,
                "name": product1.name,
                "product_uom": uom_unit.id,
                "location_id": stock_location.id,
                "location_dest_id": customer_location.id,
                "product_uom_qty": 1,
            }
        )

    def test_stock_move_date_set_to_date_stock_move(self):
        self.picking.date_stock_move = Datetime.now()
        self.picking.action_confirm()
        self.move.quantity_done = 1
        self.picking.action_done()
        self.assertEqual(self.move.date, self.picking.date_stock_move)

    def test_stock_move_date_set_to_date_done(self):
        self.picking.action_confirm()
        self.move.quantity_done = 1
        self.picking.action_done()
        self.assertEqual(self.move.date, self.picking.date_done)

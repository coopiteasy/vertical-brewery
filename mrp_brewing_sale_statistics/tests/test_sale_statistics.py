# Copyright 2021 Coop IT Easy SC
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from datetime import datetime, timedelta

from odoo.tests.common import TransactionCase


class TestSaleAnalytics(TransactionCase):
    def setUp(self):
        super(TestSaleAnalytics, self).setUp()
        self.sale_order_obj = self.env["sale.order"]
        self.partner = self.env.ref("base.res_partner_12")
        self.beer_product = self.browse_ref(
            "mrp_brewing.demo_product_product_roublarde"
        )
        self.crate_product = self.env["product.product"].create(
            {
                "name": "Beer Crate",
                "categ_id": self.ref("product.product_category_3"),
                "is_crate": True,
            }
        )
        today = datetime.today()
        self.sale_order_1 = self.sale_order_obj.create(
            {
                "partner_id": self.partner.id,
                "date_order": today - timedelta(days=1),
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "name": self.crate_product.name,
                            "product_id": self.crate_product.id,
                            "product_uom_qty": 5.0,
                            "product_uom": self.crate_product.uom_po_id.id,
                            "price_unit": 10.0,
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "name": self.beer_product.name,
                            "product_id": self.beer_product.id,
                            "product_uom_qty": 20.0,
                            "product_uom": self.beer_product.uom_po_id.id,
                            "price_unit": 1.0,
                        },
                    ),
                ],
            }
        )
        self.sale_order_1.action_confirm()
        self.sale_order_1.action_invoice_create()
        self.sale_order_2 = self.sale_order_obj.create(
            {
                "partner_id": self.partner.id,
                "date_order": today - timedelta(days=40),
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "name": self.crate_product.name,
                            "product_id": self.crate_product.id,
                            "product_uom_qty": 5.0,
                            "product_uom": self.crate_product.uom_po_id.id,
                            "price_unit": 10.0,
                        },
                    )
                ],
            }
        )
        self.sale_order_2.action_confirm()
        self.sale_order_2.action_invoice_create()
        self.sale_order_3 = self.sale_order_obj.create(
            {
                "partner_id": self.partner.id,
                "date_order": today - timedelta(days=75),
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "name": self.crate_product.name,
                            "product_id": self.crate_product.id,
                            "product_uom_qty": 11.0,
                            "product_uom": self.crate_product.uom_po_id.id,
                            "price_unit": 10.0,
                        },
                    )
                ],
            }
        )
        self.sale_order_3.action_confirm()
        self.sale_order_3.action_invoice_create()
        self.sale_order_4 = self.sale_order_obj.create(
            {
                "partner_id": self.partner.id,
                "date_order": today - timedelta(days=370),
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "name": self.crate_product.name,
                            "product_id": self.crate_product.id,
                            "product_uom_qty": 5.0,
                            "product_uom": self.crate_product.uom_po_id.id,
                            "price_unit": 10.0,
                        },
                    )
                ],
            }
        )
        self.sale_order_4.action_confirm()
        self.sale_order_4.action_invoice_create()

    def test_sale_statistics(self):

        self.assertEqual(self.partner.last_order, self.sale_order_1.date_order)
        self.assertEqual(self.partner.sale_frequency, 37)
        self.assertEqual(self.partner.crate_per_order, 7)
        self.assertEqual(self.partner.crate_per_month, 10.5)

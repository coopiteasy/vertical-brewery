# Copyright 2021 Coop IT Easy SCRL fs
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.exceptions import UserError
from odoo.fields import Date, Datetime
from odoo.tests.common import Form

from .test_mrp_brewing_base import TestMRPBrewingBase


class TestBrewDeclaration(TestMRPBrewingBase):
    def test_brew_declaration_action_cancel_draft_confirm(self):
        """Test on `brew.declaration`
        - `action_cancel`
        - `action_draft`
        - `action_confirm`
        """
        brew_declaration = self.brew_declaration_model.create(
            {"request_date": Date.today()}
        )
        # `draft` = default state
        self.assertEqual(brew_declaration.state, "draft")

        # cancel it
        brew_declaration.action_cancel()
        self.assertEqual(brew_declaration.state, "cancel")

        # change it back to draft
        brew_declaration.action_draft()
        self.assertEqual(brew_declaration.state, "draft")

        # confirm it
        brew_declaration.action_confirm()
        self.assertEqual(brew_declaration.state, "confirm")

    def test_brew_order_action_cancel_draft_confirm(self):
        """Test on `brew.order`
        - `action_cancel`
        - `action_draft`
        - `action_confirm`
        """
        brew_order = self.brew_order_model.create(
            {
                "product_id": self.product_manuf.id,
                "product_qty": 100,
                "product_uom_id": self.uom_unit.id,
                "start_date": Datetime.now(),
                "wort_gathering_date": Datetime.now(),
                "end_date": Datetime.now(),
            }
        )
        # `draft` = default state
        self.assertEqual(brew_order.state, "draft")

        # cancel it
        brew_order.action_cancel()
        self.assertEqual(brew_order.state, "cancel")

        # change it back to draft
        brew_order.action_draft()
        self.assertEqual(brew_order.state, "draft")

        # confirm it without BoM
        with self.assertRaises(UserError):
            brew_order.action_confirm()

        # confirm it with BoM
        self.mrp_bom_model.create(
            {
                "product_id": self.product_manuf.id,
                "product_tmpl_id": self.product_manuf.product_tmpl_id.id,
                "bom_line_ids": (
                    [
                        (
                            0,
                            0,
                            {
                                "product_id": self.product_raw_material.id,
                                "product_qty": 1,
                                "product_uom_id": self.uom_unit.id,
                            },
                        ),
                    ]
                ),
            }
        )
        brew_order.action_confirm()
        self.assertEqual(brew_order.state, "done")
        # TODO: assert production_order_id

    def test_cover_brew_declaration_flow(self):
        self.brew_declaration.action_confirm()
        self.brew_order.action_confirm()
        beer_mo = self.brew_order.production_order_id
        self.assertTrue(beer_mo, "green beer manufacturing order was generated")
        wort_mo = self.mrp_production_model.search([("origin", "=", beer_mo.name)])
        self.assertTrue(wort_mo, "wort manufacturing order was generated")

        # Produce Wort
        # note: when following the flow through the interface,
        #  open_produce_product opens the produce wizard.
        #  We have to open it w/ Form in tests to mimic that
        #  behavior. It is not enough to just use Form because
        #  we need to go through open_produce_product to set
        #  the master_mo_id field.

        produce_action = wort_mo.with_context(
            {
                "active_id": wort_mo.id,
                "active_ids": [wort_mo.id],
            }
        ).open_produce_product()
        produce_form = Form(
            self.env[produce_action["res_model"]].with_context(
                {
                    "active_id": wort_mo.id,
                    "active_ids": [wort_mo.id],
                }
            )
        )
        produce_form.product_qty = 1.0
        produce_wiz = produce_form.save()
        malt_line = produce_wiz.produce_line_ids.filtered(
            lambda l: l.product_id == self.malt_product
        )
        malt_line.lot_id = self.browse_ref("mrp_brewing.demo_lot_malt")
        produce_wiz.do_produce()
        wort_mo.button_mark_done()
        self.assertEqual(
            wort_mo.state, "done", "Production order should be in done state."
        )

        wort_mo = self.mrp_production_model.search([("master_mo_id", "=", beer_mo.id)])
        self.assertTrue(wort_mo, "wort manufacturing order was generated")

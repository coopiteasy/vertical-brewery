# Copyright 2021 Coop IT Easy SCRL fs
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from .test_mrp_brewing_base import TestMRPBrewingBase


class TestMRPProduction(TestMRPBrewingBase):
    def test_master_manufacturing_order_computation(self):
        # brew order for 'Roublarde Green Beer'
        self.brew_order.action_confirm()
        master_mo = self.brew_order.production_order_id
        self.assertFalse(master_mo.master_mo_id)
        # should generate MO for Roublarde Wort
        self.assertEquals(len(master_mo.child_mo_ids), 1)
        # should set the master_mo_id of the children
        self.assertEquals(master_mo.child_mo_ids.master_mo_id, master_mo)

    def test_manual_master_manufacturing_order(self):
        self.brew_order.action_confirm()
        master_mo = self.brew_order.production_order_id
        # create a new mrp.production, setting the master manufacturing order
        # manually
        mrp_production = self.mrp_production_model.create({
            "product_id": self.green_beer_product.id,
            "product_qty": 1,
            "product_uom_id": self.uom_litre.id,
            "bom_id": self.brew_order.bom.id,
            "master_mo_id": master_mo.id,
        })
        self.assertEquals(mrp_production.master_mo_id, master_mo)

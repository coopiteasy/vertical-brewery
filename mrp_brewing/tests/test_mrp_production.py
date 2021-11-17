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

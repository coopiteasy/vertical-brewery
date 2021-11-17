# Copyright 2021 Coop IT Easy SCRL fs
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).


from odoo.fields import Date, Datetime
from odoo.tests.common import TransactionCase


class TestMRPBrewingBase(TransactionCase):
    def setUp(self, *args, **kwargs):
        super(TestMRPBrewingBase, self).setUp(*args, **kwargs)
        self.brew_declaration_model = self.env["brew.declaration"]
        self.brew_order_model = self.env["brew.order"]
        self.mrp_production_model = self.env["mrp.production"]
        self.mrp_bom_model = self.env["mrp.bom"]
        self.uom_unit = self.env.ref("uom.product_uom_unit")
        self.uom_litre = self.env.ref("uom.product_uom_litre")

        # generate stock
        inventory = self.browse_ref("mrp_brewing.demo_stock_inventory_0")
        inventory.action_start()
        inventory.action_validate()

        self.malt_product = self.browse_ref("mrp_brewing.demo_product_product_malt")
        self.green_beer_product = self.browse_ref(
            "mrp_brewing.demo_product_product_green_beer"
        )

        self.product_manuf = self.env["product.product"].create(
            {
                "name": "Manuf",
                "type": "product",
                "uom_id": self.uom_unit.id,
                "is_brewable": True,
                "brew_product_sequence": self.env["ir.sequence"]
                .create(
                    {
                        "name": "Brew Product Sequence",
                    }
                )
                .id,
            }
        )

        self.product_raw_material = self.env["product.product"].create(
            {
                "name": "Beer Raw Material",
                "type": "product",
                "uom_id": self.uom_unit.id,
                "raw_material": True,
            }
        )

        self.brew_declaration = self.brew_declaration_model.create(
            {"request_date": Date.today()}
        )

        self.brew_order = self.brew_order_model.create(
            {
                "product_id": self.green_beer_product.id,
                "product_qty": 200,
                "product_uom_id": self.uom_litre.id,
                "start_date": Datetime.now().replace(hour=9),
                "wort_gathering_date": Datetime.now().replace(hour=18),
                "end_date": Datetime.now().replace(hour=10),
                "brew_declaration_id": self.brew_declaration.id,
            }
        )

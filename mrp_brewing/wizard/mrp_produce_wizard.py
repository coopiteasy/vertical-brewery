from odoo import api, fields, models


class MRPProductProduce(models.TransientModel):
    _inherit = "mrp.product.produce"

    @api.model
    def _create_production_lot(self):
        mo_obj = self.env["mrp.production"]

        manufacturing_order = mo_obj.browse(self._context["active_id"])
        # previous lot may exist if produce wizard was closed
        product_lot = self.env["stock.production.lot"].search(
            [
                ("name", "=", manufacturing_order.brew_order_name),
                ("product_id", "=", manufacturing_order.product_id.id),
            ],
            limit=1,
        )

        if product_lot:
            return product_lot.id

        vals = {
            "name": manufacturing_order.brew_order_name,
            "product_id": manufacturing_order.product_id.id,
        }
        return self.env["stock.production.lot"].create(vals).id

    # Should only be visible when it is consume and produce mode
    lot_id = fields.Many2one(default=_create_production_lot)

from odoo import api, fields, models


class MRPProductProduce(models.TransientModel):
    _inherit = "mrp.product.produce"

    @api.model
    def _create_production_lot(self):
        mo_obj = self.env["mrp.production"]

        manufacturing_order = mo_obj.browse(self._context["active_id"])
        # when does this happen ? The lot is created at all times
        product_lot = self.env["stock.production.lot"].search(
            [
                ("name", "=", manufacturing_order.brew_order_name),
                ("product_id", "=", manufacturing_order.product_id.id),
            ]
        )

        if len(product_lot) > 0:
            return product_lot.id

        vals = {
            "name": manufacturing_order.brew_order_name,
            "product_id": manufacturing_order.product_id.id,
        }
        return self.env["stock.production.lot"].create(vals).id

    # Should only be visible when it is consume and produce mode
    lot_id = fields.Many2one(
        "stock.production.lot", "Lot", default=_create_production_lot
    )

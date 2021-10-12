# Copyright 2021 Coop IT Easy SCRL fs
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class StockReport(models.TransientModel):
    _name = "stock.report"
    _description = "Stock Report"

    report = fields.Selection(
        [
            ("raw_materials", "Raw Material Report"),
            (
                "finished_products",
                "Finished Product Report",
            ),
            (
                "brew_register",
                " Brew Register Report",
            ),
        ],
        string="Report Name",
        required=True,
    )
    date_from = fields.Date(string="Start Date")
    date_to = fields.Date(string="End Date")

    @api.multi
    def create_report(self):
        self.ensure_one()
        if self.report == "raw_materials":
            action = "mrp_brewing.action_raw_materials_report"
            recordset = self.env["stock.move"].search(
                [("state", "=", "done"), ("product_id.raw_material", "=", True)],
                order="date asc",
            )
        elif self.report == "finished_products":
            action = "mrp_brewing.action_finished_products_report"
            recordset = self.env["stock.move"].search(
                [
                    ("state", "=", "done"),
                    ("product_id.finished_product", "=", True),
                ],
                order="date asc",
            )
        else:  # brew_register
            action = "mrp_brewing.action_brew_register_report"
            recordset = self.env["brew.order"].search([("state", "=", "done")])

        return self.env.ref(action).report_action(recordset)

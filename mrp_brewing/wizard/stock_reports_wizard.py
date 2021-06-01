from odoo import api, fields, models

MODEL_MAP = {
    "mrp_brewing.action_raw_materials_report": "stock.move",
    "mrp_brewing.action_finished_products_report": "stock.move",
    "mrp_brewing.action_brew_register_report": "brew.order",
}


class StockReport(models.TransientModel):
    _name = "stock.report"
    _description = "Stock Report"

    report_name = fields.Selection(
        [
            ("mrp_brewing.action_raw_materials_report", "Raw Material Report"),
            (
                "mrp_brewing.action_finished_products_report",
                "Finished Product Report",
            ),
            (
                "mrp_brewing.action_brew_register_report",
                " Brew Register Report",
            ),
        ],
        string="Report Name",
        required=True,
    )
    date_from = fields.Date(string="Start Date")
    date_to = fields.Date(string="End Date")

    def _build_contexts(self, data):
        result = {}
        result["date_from"] = data["form"]["date_from"] or False
        result["date_to"] = data["form"]["date_to"] or False
        result["strict_range"] = True if result["date_from"] else False
        return result

    @api.multi
    def check_report(self):
        self.ensure_one()
        data = {}
        data["ids"] = self.env.context.get("active_ids", [])
        data["model"] = MODEL_MAP[self.report_name]
        data["form"] = self.read(["date_from", "date_to"])[0]
        used_context = self._build_contexts(data)
        data["form"]["used_context"] = dict(
            used_context, lang=self.env.context.get("lang", "en_US")
        )
        # return self.env["report"].get_action(self, self.report_name, data=data)
        return self.env.ref(self.report_name).report_action(self, data=data)

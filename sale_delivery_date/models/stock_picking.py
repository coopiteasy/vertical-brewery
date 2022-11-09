# Part of Open Architechts Consulting sprl. See LICENSE file for full copyright and licensing details. # noqa
# Copyright 2019 Coop IT Easy SC

from odoo import api, fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    date_stock_move = fields.Datetime(
        string="Date of Transfer ", states={"done": [("readonly", True)]}
    )

    @api.multi
    def action_done(self):
        super(StockPicking, self).action_done()
        for picking in self:
            if not picking.date_stock_move:
                picking.date_stock_move = fields.Datetime.now()

            for move in picking.move_lines:
                move.date = picking.date_stock_move

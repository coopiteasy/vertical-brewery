# Part of Open Architechts Consulting sprl. See LICENSE file for full copyright and licensing details. # noqa
# Copyright 2019 Coop IT Easy SCRLfs

from odoo import api, fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    # Used to force the date of the moves to a specific date
    #   in the xml form view (view_picking_form), the field name
    #   of date_done(string="Date of Transfer") is overloaded with
    #   Effective Date. This is confusing.
    #   The field scheduled_date adds to the confusion...
    date_stock_move = fields.Datetime(
        string="Date of Transfer ", states={"done": [("readonly", True)]}
    )

    # todo move to custom module
    @api.multi
    def action_done(self):
        super(StockPicking, self).action_done()
        for picking in self:
            for move in picking.move_lines:
                if picking.date_stock_move:
                    move.date = picking.date_stock_move
                else:
                    move.date = picking.date_done

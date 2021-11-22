# Copyright 2021 Coop IT Easy SCRL fs
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Sale Delivery Date",
    "summary": "Track delivery date and status from sale orders.",
    "category": "Stock",
    "version": "12.0.1.0.0",
    "author": "Coop IT Easy SCRLfs",
    "website": "https://github.com/coopiteasy/vertical-brewery",
    "license": "AGPL-3",
    "depends": ["sale_stock"],
    "data": [
        "views/sale_order_views.xml",
        "views/stock_picking_views.xml",
        "reports/report_deliveryslip.xml",
    ],
    "installable": True,
}

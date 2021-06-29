# © 2016-2018 Open Architects Consulting SPRL.
# © 2018 Coop IT Easy SCRLfs. (<http://www.coopiteasy.be>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "MRP Brewing - Sale Analytics",
    "summary": "Adds brewery related sale metrics.",
    "category": "Stock",
    "version": "12.0.1.0.0",
    "author": "Coop IT Easy SCRLfs",
    "website": "https://github.com/OCA/sale-workflow",
    "license": "AGPL-3",
    "depends": [
        "mrp_brewing",
    ],
    "data": [
        "data/cron.xml",
        "views/res_partner_view.xml",
    ],
    "installable": True,
}

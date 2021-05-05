# © 2016-2018 Open Architects Consulting SPRL.
# © 2018 Coop IT Easy SCRLfs. (<http://www.coopiteasy.be>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "MRP Brewing",
    "summary": "This module allows to handle product transformation",
    "category": "Stock",
    "version": "11.0.1.0.0",
    "author": "Coop IT Easy SCRLfs",
    "website": "https://coopiteasy.be",
    "license": "AGPL-3",
    "depends": [
        "mrp_byproduct",
        "stock",
        "sale",
        "product",
        "sale_order_dates",
        "purchase",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/brewing_data.xml",
        "data/cron.xml",
        "report/report_stock_raw_materials.xml",
        "report/report_stock_finished_products.xml",
        "report/report_brew_register.xml",
        "report/report_stock.xml",
        "report/report_layout.xml",
        "wizard/stock_reports_view.xml",
        "wizard/recompute_qty_afte_move_view.xml",
        "views/product_template_views.xml",
        "views/purchase_views.xml",
        "views/product_pricelist_views.xml",
        "views/mrp_production_views.xml",
        "views/brew_declaration_views.xml",
        "views/brew_order_views.xml",
        "views/stock_warehouse_views.xml",
        "views/stock_quant_views.xml",
        "views/stock_production_lot_views.xml",
        "views/stock_pack_operation_views.xml",
        "views/stock_picking_views.xml",
        "views/stock_move_views.xml",
        "views/sale_views.xml",
        "views/sale_order_report.xml",
        "views/res_partner_view.xml",
        "views/res_company_view.xml",
    ],
    "application": True,
    "installable": True,
}

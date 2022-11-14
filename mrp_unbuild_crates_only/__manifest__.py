# Copyright 2022 Coop IT Easy SC
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Unbuild crates only",
    "summary": "List only crates when creating an unbuild order",
    "version": "12.0.1.0.1",
    "category": "Manufacturing",
    "website": "https://github.com/coopiteasy/vertical-brewery",
    "author": "Coop IT Easy SC",
    "license": "AGPL-3",
    "application": False,
    "depends": [
        "mrp_brewing",
        "mrp_unbuild_product_mo_filter",
    ],
    "excludes": [],
    "data": [
        "views/mrp_unbuild.xml",
    ],
    "demo": [],
    "qweb": [],
}

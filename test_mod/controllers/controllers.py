# controllers.py
from odoo import http
from odoo.http import request


class OdooController(http.Controller):
    @http.route("/dev/controller/", auth="public", website=True)
    def index(self, **kw):
        sales_orders = http.request.env["sale.order"].search([])
        output = "<h1>Sales Orders</h1><ul>"
        for sale in sales_orders:
            output += "<li>" + sale["name"] + "</li>"
            print(sale["name"])
        output += "</ul>"
        # return "<h1>Data Accessed</h1>"
        return output

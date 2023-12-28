# controllers.py
from odoo import http
from odoo.http import request


class OdooController(http.Controller):
    @http.route("/dev/omhosp/", auth="public", website=True)
    def index(self, **kw):
        hospital_patient = http.request.env["hospital.patient"].search([])
        output = "<h1>Patient List</h1><ul>"
        for patient in hospital_patient:
            output += "<li>" + patient["gender"] + "</li>"
            print(patient["gender"])
        output += "</ul>"
        # return "<h1>Data Accessed</h1>"
        return output

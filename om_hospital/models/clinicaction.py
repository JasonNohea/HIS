from odoo import models, fields, api


class ClinicAction(models.Model):
    _name = "clinic.action"
    _inherit = ["mail.thread"]
    _description = "Clinic Action"

    name = fields.Char(string="Name")
    cost = fields.Float(string="Cost")
    description = fields.Text(string="Description")
    status = fields.Selection(
        [("available", "Available"), ("not available", "Not Available")],
        string="Status",
        default="available",
        required=True,
    )
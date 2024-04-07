from odoo import models, fields, api


class nurse(models.Model):
    _name = "clinic.action"
    _inherit = ["mail.thread"]
    _description = "Clinic Action"

    name = fields.Char(string="Name")
    description = fields.Text(string="Description")
    status = fields.Selection(
        [("working", "working"), ("standby", "On Standby")],
        string="Status",
        default="standby",
        required=True,
    )

from odoo import models, fields, api


class nurse(models.Model):
    _name = "clinic.rooms"
    _inherit = ["mail.thread"]
    _description = "Clinic Rooms"

    name = fields.Char(string="Name")
    description = fields.Text(string="Description")
    status = fields.Selection(
        [("working", "working"), ("standby", "On Standby")],
        string="Status",
        default="standby",
        required=True,
    )

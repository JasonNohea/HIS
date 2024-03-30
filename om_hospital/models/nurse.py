from odoo import models, fields, api


class nurse(models.Model):
    _name = "clinic.nurse"
    _inherit = ["mail.thread"]
    _description = "Clinic Nurse"

    name = fields.Char(string="Name")
    photo = fields.Binary(string="Photo")
    phone = fields.Char(string="Phone Number", tracking=True)
    email = fields.Char(string="Email", help="Enter email address", widget="email")
    address = fields.Text(string="Address", required=True, tracking=True)
    place_of_birth = fields.Char(string="Place of Birth", required=True, tracking=True)
    description = fields.Text(string="Description")
    gender = fields.Selection(
        [("male", "Male"), ("female", "Female"), ("others", "Others")],
        string="Gender",
        tracking=True,
    )
    status = fields.Selection(
        [("working", "working"), ("standby", "On Standby")],
        string="Status",
        default="standby",
        required=True,
    )

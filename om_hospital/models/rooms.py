from odoo import models, fields, api


class nurse(models.Model):
    _name = "clinic.rooms"
    _inherit = ["mail.thread"]
    _description = "Clinic Rooms"

    name = fields.Char(string="Name")
    type = fields.Selection(
        [
            ("examination", "Examination Room"),
            ("consultaion", "Consultaion Room"),
            ("emergency", "Emergency Room"),
            ("treatment", "Treatment Room"),
            ("patient", "Patient Room"),
        ],
        string="Room Type",
    )
    capacity = fields.Integer(string="Capacity")
    equipment = fields.Many2many("clinic.equipment", string="Equipment Available")
    description = fields.Text(string="Description")
    status = fields.Selection(
        [
            ("vacant", "Vacant"),
            ("occupied", "Occupied"),
            ("unavailable", "Unavailable"),
        ],
        string="Status",
        default="vacant",
        required=True,
    )

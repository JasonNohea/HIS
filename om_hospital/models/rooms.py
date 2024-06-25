from odoo import models, fields, api


class ClinicRoom(models.Model):
    _name = "clinic.rooms"
    _inherit = ["mail.thread"]
    _description = "Clinic Rooms"

    name = fields.Char(string="Name", tracking=True)
    type = fields.Selection(
        [
            ("examination", "Examination Room"),
            ("consultation", "Consultation Room"),
            ("emergency", "Emergency Room"),
            ("treatment", "Treatment Room"),
            ("patient", "Patient Room"),
        ],
        string="Room Type",
        tracking=True,
    )
    capacity = fields.Integer(string="Capacity", tracking=True)
    equipment = fields.Many2many(
        "clinic.equipment", string="Equipment Available", tracking=True
    )
    description = fields.Text(string="Description", tracking=True)
    status = fields.Selection(
        [
            ("vacant", "Vacant"),
            ("occupied", "Occupied"),
            ("unavailable", "Unavailable"),
        ],
        string="Status",
        default="vacant",
        tracking=True,
    )

    @api.model
    def create_predefined_rooms(self):
        predefined_rooms = [
            {
                "name": "Examination Room 1",
                "type": "examination",
                "capacity": 1,
                "description": "Used for patient examinations.",
                "status": "vacant",
            },
            {
                "name": "Consultation Room 1",
                "type": "consultation",
                "capacity": 1,
                "description": "Used for patient consultations.",
                "status": "vacant",
            },
            {
                "name": "Emergency Room 1",
                "type": "emergency",
                "capacity": 2,
                "description": "Used for emergency treatments.",
                "status": "vacant",
            },
            {
                "name": "Treatment Room 1",
                "type": "treatment",
                "capacity": 1,
                "description": "Used for treatments and minor procedures.",
                "status": "vacant",
            },
            {
                "name": "Patient Room 1",
                "type": "patient",
                "capacity": 2,
                "description": "Used for patient stays.",
                "status": "vacant",
            },
            {
                "name": "Examination Room 2",
                "type": "examination",
                "capacity": 1,
                "description": "Used for patient examinations.",
                "status": "vacant",
            },
            {
                "name": "Consultation Room 2",
                "type": "consultation",
                "capacity": 1,
                "description": "Used for patient consultations.",
                "status": "vacant",
            },
            {
                "name": "Emergency Room 2",
                "type": "emergency",
                "capacity": 2,
                "description": "Used for emergency treatments.",
                "status": "vacant",
            },
            {
                "name": "Treatment Room 2",
                "type": "treatment",
                "capacity": 1,
                "description": "Used for treatments and minor procedures.",
                "status": "vacant",
            },
            {
                "name": "Patient Room 2",
                "type": "patient",
                "capacity": 2,
                "description": "Used for patient stays.",
                "status": "vacant",
            },
            {
                "name": "Examination Room 3",
                "type": "examination",
                "capacity": 1,
                "description": "Used for patient examinations.",
                "status": "vacant",
            },
            {
                "name": "Consultation Room 3",
                "type": "consultation",
                "capacity": 1,
                "description": "Used for patient consultations.",
                "status": "vacant",
            },
            {
                "name": "Emergency Room 3",
                "type": "emergency",
                "capacity": 2,
                "description": "Used for emergency treatments.",
                "status": "vacant",
            },
            {
                "name": "Treatment Room 3",
                "type": "treatment",
                "capacity": 1,
                "description": "Used for treatments and minor procedures.",
                "status": "vacant",
            },
            {
                "name": "Patient Room 3",
                "type": "patient",
                "capacity": 2,
                "description": "Used for patient stays.",
                "status": "vacant",
            },
        ]
        for room in predefined_rooms:
            self.create(room)

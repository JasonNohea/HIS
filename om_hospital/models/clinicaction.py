from odoo import models, fields, api
import random


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

    @api.model
    def create_random_actions(self, num_records=5):
        predefined_actions = [
            {
                "name": "Blood Test",
                "cost": 50.0,
                "description": "Routine blood test",
                "status": "available",
            },
            {
                "name": "X-Ray",
                "cost": 100.0,
                "description": "Standard X-ray imaging",
                "status": "available",
            },
            {
                "name": "MRI Scan",
                "cost": 300.0,
                "description": "Magnetic Resonance Imaging",
                "status": "available",
            },
            {
                "name": "CT Scan",
                "cost": 250.0,
                "description": "Computed Tomography Scan",
                "status": "available",
            },
            {
                "name": "Ultrasound",
                "cost": 150.0,
                "description": "Ultrasound imaging",
                "status": "available",
            },
        ]
        for action in predefined_actions[:num_records]:
            self.create(action)

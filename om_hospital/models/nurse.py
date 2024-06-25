from odoo import models, fields, api
from odoo.exceptions import ValidationError
import random
import datetime
import re


class Nurse(models.Model):
    _name = "clinic.nurse"
    _inherit = ["mail.thread"]
    _description = "Clinic Nurse"

    name = fields.Char(string="Name", tracking=True, store=True)
    photo = fields.Binary(string="Photo")
    phone = fields.Char(string="Phone Number", tracking=True)
    email = fields.Char(string="Email", help="Enter email address", widget="email")
    address = fields.Text(string="Address", tracking=True)
    place_of_birth = fields.Char(string="Place of Birth", tracking=True)
    description = fields.Text(string="Description")
    gender = fields.Selection(
        [("male", "Male"), ("female", "Female"), ("others", "Others")],
        string="Gender",
        tracking=True,
    )
    status = fields.Selection(
        [("working", "Working"), ("standby", "On Standby"), ("offduty", "Off Duty")],
        string="Status",
        default="standby",
    )
    date_of_birth = fields.Date(string="Date of Birth", tracking=True)
    marital_status = fields.Selection(
        [
            ("married", "Married"),
            ("single", "Single"),
            ("divorced", "Divorced"),
            ("widow", "Widow"),
            ("widower", "Widower"),
        ],
        string="Marital Status",
        tracking=True,
    )
    nursing_license_num = fields.Char(string="Nursing License Number", tracking=True)
    experience = fields.Integer(string="Years of Experience", tracking=True)
    education = fields.Char(string="Education Background", tracking=True)
    work_history = fields.Text(string="Work History")

    @api.constrains("email")
    def _check_valid_email(self):
        for record in self:
            if record.email:
                if not re.match(r"[^@]+@[^@]+\.[^@]+", record.email):
                    raise ValidationError("Invalid email address: %s" % record.email)

    @api.model
    def create_random_nurses(self, num_records=5):
        for _ in range(num_records):
            self.create(
                {
                    "name": self._get_random_name(),
                    "photo": False,
                    "phone": self._get_random_phone(),
                    "email": self._get_random_email(),
                    "address": self._get_random_address(),
                    "place_of_birth": self._get_random_city(),
                    "description": self._get_random_description(),
                    "gender": random.choice(["male", "female", "others"]),
                    "status": random.choice(["working", "standby", "offduty"]),
                }
            )

    def _get_random_name(self):
        return random.choice(
            ["John Doe", "Jane Smith", "Alice Johnson", "Bob Brown", "Chris White"]
        )

    def _get_random_phone(self):
        return "123-456-7890"

    def _get_random_email(self):
        return "example@example.com"

    def _get_random_address(self):
        return "123 Main St, Anytown, USA"

    def _get_random_city(self):
        return random.choice(
            ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix"]
        )

    def _get_random_description(self):
        return "Dedicated and experienced nurse."

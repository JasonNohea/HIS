# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
import random
import datetime
import re


# creating databased
class ClinicDoctor(models.Model):
    _name = "clinic.doctor"
    _inherit = ["mail.thread"]
    _description = "Clinic Doctor"

    name = fields.Char(string="Name", tracking=True, store=True)
    photo = fields.Binary(string="Photo")
    specialization = fields.Char(string="Specialization", tracking=True)
    description = fields.Text(string="Description")
    phone = fields.Char(string="Phone Number", tracking=True)
    email = fields.Char(string="Email", help="Enter email address", widget="email")
    address = fields.Text(string="Address", required=False, tracking=True)
    place_of_birth = fields.Char(string="Place of Birth", tracking=True)
    medical_license_num = fields.Char(string="Medical License Number", tracking=True)
    experience = fields.Integer(string="Years of Experience", tracking=True)
    education = fields.Char(string="Education Background", tracking=True)
    work_history = fields.Text(string="Work History")
    date_of_birth = fields.Date(
        string="Date of Birth",
        default=False,
        # default=lambda self: fields.Date.today(),
        # Add a domain to restrict the date range
        # domain="[('date', '<=', fields.Date.today())]",
    )
    gender = fields.Selection(
        [("male", "Male"), ("female", "Female"), ("others", "Others")],
        string="Gender",
        tracking=True,
    )
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
    status = fields.Selection(
        [("working", "working"), ("standby", "On Standby"), ("off_duty", "Off Duty")],
        string="Status",
        default="standby",
    )

    @api.constrains("email")
    def _check_valid_email(self):
        for record in self:
            if record.email:
                if not re.match(r"[^@]+@[^@]+\.[^@]+", record.email):
                    raise ValidationError("Invalid email address: %s" % record.email)

    # @api.depends("service")
    # def _fetch_service(self):
    #     for rec in self:
    #         if rec.service:
    #             rec.name = rec.service
    #         else:
    #             rec.name = ""
    @api.model
    def create_random_doctors(self, num_records=5):
        for _ in range(num_records):
            self.create(
                {
                    "name": self._get_random_name(),
                    "specialization": self._get_random_specialization(),
                    "description": self._get_random_description(),
                    "phone": self._get_random_phone(),
                    "email": self._get_random_email(),
                    "address": self._get_random_address(),
                    "place_of_birth": self._get_random_city(),
                    "medical_license_num": self._get_random_medical_license_num(),
                    "experience": random.randint(1, 40),
                    "education": self._get_random_education(),
                    "work_history": self._get_random_work_history(),
                    "date_of_birth": self._get_random_date_of_birth(),
                    "gender": random.choice(["male", "female", "others"]),
                    "marital_status": random.choice(
                        ["married", "single", "divorced", "widow", "widower"]
                    ),
                    "status": random.choice(["working", "standby", "off_duty"]),
                }
            )

    def _get_random_name(self):
        return random.choice(
            ["John Doe", "Jane Smith", "Alice Johnson", "Bob Brown", "Chris White"]
        )

    def _get_random_specialization(self):
        return random.choice(
            ["Cardiology", "Dermatology", "Neurology", "Pediatrics", "Surgery"]
        )

    def _get_random_description(self):
        return "Experienced and dedicated medical professional."

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

    def _get_random_medical_license_num(self):
        return "ABCD-12345678"

    def _get_random_education(self):
        return "Medical School, University of Medicine"

    def _get_random_work_history(self):
        return "Worked at various renowned hospitals."

    def _get_random_date_of_birth(self):
        start_date = datetime.date(1950, 1, 1)
        end_date = datetime.date(1999, 12, 31)
        time_between_dates = end_date - start_date
        days_between_dates = time_between_dates.days
        random_number_of_days = random.randrange(days_between_dates)
        random_date = start_date + datetime.timedelta(days=random_number_of_days)
        return random_date

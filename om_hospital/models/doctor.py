# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


# creating databased
class ClinicDoctor(models.Model):
    _name = "clinic.doctor"
    _inherit = ["mail.thread"]
    _description = "Clinic Doctor"

    name = fields.Char(string="Name", tracking=True, store=True)
    photo = fields.Binary(string="Photo")
    specialization = fields.Char(string="Specialization", required=True, tracking=True)
    description = fields.Text(string="Description")
    phone = fields.Char(string="Phone Number", tracking=True)
    address = fields.Text(string="Address", required=True, tracking=True)
    place_of_birth = fields.Char(string="Place of Birth", required=True, tracking=True)
    medical_license_num = fields.Char(string="Medical License Number", tracking=True)
    experience = fields.Integer(string="Years of Experience", tracking=True)
    education = fields.Char(string="Education Background", tracking=True)
    work_history = fields.Text(string="Work History")
    date_of_birth = fields.Date(
        string="Date of Birth",
        default=False,
        required=True,
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
        [("working", "working"), ("standby", "On Standby")],
        string="Status",
        default="standby",
        required=True,
    )

    # @api.depends("service")
    # def _fetch_service(self):
    #     for rec in self:
    #         if rec.service:
    #             rec.name = rec.service
    #         else:
    #             rec.name = ""

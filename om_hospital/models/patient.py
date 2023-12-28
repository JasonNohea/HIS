# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


# creating databased
class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _inherit = ["mail.thread"]
    _description = "Patient Records"

    name = fields.Char(string="Name", required=True, tracking=True)
    place_of_birth = fields.Char(string="Place of Birth", required=True, tracking=True)
    date_of_birth = fields.Date(
        string="Date of Birth",
        default=False,
        # default=lambda self: fields.Date.today(),
        # Add a domain to restrict the date range
        # domain="[('date', '<=', fields.Date.today())]",
    )
    address = fields.Text(string="Address", required=True, tracking=True)
    residential_code = fields.Char(
        string="Neighborhood (RT)", tracking=True
    )  # required=True,
    neighborhood_code = fields.Char(
        string="Hamlet (RW)", tracking=True
    )  # required=True,
    sub_district = fields.Char(
        string="Urban village (Kelurahan)", tracking=True
    )  # required=True,
    district_municipality = fields.Char(
        string="Sub-district (Kecamatan)", tracking=True
    )  # required=True,
    phone = fields.Char(string="Phone Number", tracking=True)
    age = fields.Integer(string="Age", tracking=True)
    is_child = fields.Boolean(string="Is Child?", tracking=True)
    notes = fields.Text(string="Notes")
    gender = fields.Selection(
        [("male", "Male"), ("female", "Female"), ("others", "Others")],
        string="Gender",
        tracking=True,
    )
    religion = fields.Selection(
        [
            ("islam", "Islam"),
            ("catholic", "Catholic"),
            ("protestant", "Protestant"),
            ("buddha", "Buddha"),
            ("hindu", "Hindu"),
            ("others", "Others"),
        ],
        string="Religion",
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
    capitalized_name = fields.Char(
        string="Capitalized Name", compute="_compute_capitalized_name", store=True
    )  # readonly=False

    job = fields.Selection(
        [
            ("government employees", "Government Employees"),
            ("private employees", "Private Employees"),
            ("student", "Student"),
            ("college student", "College Student"),
            ("laborer", "Laborer"),
            ("housewife", "Housewife"),
            ("unemployed", "Unemployed"),
            ("Others", "Others"),
        ],
        string="Job",
        tracking=True,
    )

    payment_method = fields.Selection(
        [
            ("pay directly", "Pay Directly"),
            ("diakonia subsidies", "Diakonia Subsidies"),
            ("insurance", "Insurance"),
            ("Others", "Others"),
        ],
        string="Payment Method",
        tracking=True,
    )

    family_name = fields.Char(string="Name", required=True, tracking=True)
    family_gender = fields.Selection(
        [("male", "Male"), ("female", "Female"), ("others", "Others")],
        string="Gender",
        tracking=True,
    )
    family_relation = fields.Char(string="Relation", tracking=True)  # required=True,
    family_phone = fields.Char(string="Phone Number", tracking=True)

    @api.model_create_multi
    def create(self, vals_list):
        # Modify the values in each dictionary
        for vals in vals_list:
            vals["gender"] = "female"
        return super(HospitalPatient, self).create(vals_list)

    @api.constrains("is_child", "age")
    def _check_child_age(self):
        for rec in self:
            if rec.is_child and rec.age == 0:
                raise ValidationError(_("Age has to be recorded!"))

    @api.constrains("phone", "family_phone")
    def _check_valid_phone(self):
        for record in self:
            if record.phone and not record.phone.isdigit():
                raise ValidationError("Phone number must contain only digits.")
            if record.family_phone and not record.family_phone.isdigit():
                raise ValidationError("Family phone number must contain only digits.")

    @api.depends("name")
    def _compute_capitalized_name(self):
        for rec in self:
            if rec.name:
                rec.capitalized_name = rec.name.upper()
            else:
                rec.capitalized_name = ""

    @api.onchange("age")
    def _onchange_age(self):
        if self.age <= 10:
            self.is_child = True
        else:
            self.is_child = False

# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import date
from dateutil.relativedelta import relativedelta


# creating databased
class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _inherit = ["mail.thread"]
    _description = "Patient Records"
    # _rec_name = "ref" #if you want to the ref code to show instead of name

    name = fields.Char(string="Name", required=True, tracking=True)
    photo = fields.Binary(string="Photo")
    ref = fields.Char(string="Reference", default=lambda self: _("New"))
    place_of_birth = fields.Char(string="Place of Birth", required=True, tracking=True)
    date_of_birth = fields.Date(
        string="Date of Birth",
        default=False,
        required=True,
        # default=lambda self: fields.Date.today(),
        # Add a domain to restrict the date range
        # domain="[('date', '<=', fields.Date.today())]",
    )
    daycount = fields.Char(
        string="Day", tracking=True, compute="_datecount", store=True
    )
    monthcount = fields.Char(
        string="Month", tracking=True, compute="_datecount", store=True
    )
    yearcount = fields.Char(
        string="Year", tracking=True, compute="_datecount", store=True
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
    # age = fields.Integer(string="Age", tracking=True)
    # is_child = fields.Boolean(string="Is Child?", tracking=True)
    notes = fields.Text(string="Notes")
    gender = fields.Selection(
        [("male", "Male"), ("female", "Female"), ("others", "Others")],
        string="Gender",
        tracking=True,
    )
    bloodtype = fields.Selection(
        [
            ("A+", "A+"),
            ("B+", "B+"),
            ("O+", "O+"),
            ("AB+", "AB+"),
            ("A-", "A-"),
            ("B-", "B-"),
            ("O-", "O-"),
            ("AB-", "AB-"),
        ],
        string="Blood Type",
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
    # capitalized_name = fields.Char(
    #     string="Capitalized Name", compute="_compute_capitalized_name", store=True
    # )  # readonly=False

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

    family_name = fields.Char(string="Relative Name", tracking=True)
    family_gender = fields.Selection(
        [("male", "Male"), ("female", "Female"), ("others", "Others")],
        string="Relative Gender",
        tracking=True,
    )
    family_relation = fields.Char(
        string="Relative Relation", tracking=True
    )  # required=True,
    family_phone = fields.Char(string="Relative Phone Number", tracking=True)

    # @api.model_create_multi
    # def create(self, vals_list):
    #     # Modify the values in each dictionary
    #     for vals in vals_list:
    #         vals["ref"] = self.env["ir.sequence"].next_by_code("hospital.patient")
    #         # vals["gender"] = "female"
    #     return super(HospitalPatient, self).create(vals_list)

    # @api.model
    # def create(self, vals):
    #     if vals.get("ref", _("New")) == _("New"):
    #         vals["ref"] = self.env["ir.sequence"].next_by_code("hospital.patient") or _(
    #             "New"
    #         )
    #     return super(HospitalPatient, self).create(vals)

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

    @api.depends("date_of_birth")
    def _datecount(self):
        today = date.today()
        for record in self:
            if record.date_of_birth:
                birth_date = record.date_of_birth
                delta = relativedelta(today, birth_date)
                record.yearcount = str(delta.years) + " years"
                record.monthcount = str(delta.months) + " months"
                record.daycount = str(delta.days) + " days"

    @api.model
    def create(self, vals):
        # Generate the reference code if not provided
        if vals.get("ref", _("New")) == _("New"):
            vals["ref"] = self.env["ir.sequence"].next_by_code("hospital.patient") or _(
                "New"
            )
        # if vals.get("status") == "notcheck":
        #     vals["status"] = "frontdesk"

        # Create the patient record
        patient = super(HospitalPatient, self).create(vals)

        self.env["clinic.frontoffice"].create(
            {"name": patient.id, "status": "frontdesk"}
        )

        # Create a record in the medical.check model if it doesn't exist
        medical_check_record = self.env["medical.check"].search(
            [("name", "=", patient.id)]
        )
        if not medical_check_record:
            self.env["medical.check"].create({"name": patient.id})

        # Update the existing medical check record if it exists
        else:
            medical_check_record.write({"name": patient.id})

        # self.env["doctor.inspection"].create({"name": patient.id})

        # self.env["clinic.payment"].create({"name": patient.id})

        # Create a record in the medical.check model if it doesn't exist
        doc_inspect_record = self.env["doctor.inspection"].search(
            [("name", "=", patient.id)]
        )
        if not doc_inspect_record:
            self.env["doctor.inspection"].create({"name": patient.id})

        # Update the existing medical check record if it exists
        else:
            doc_inspect_record.write({"name": patient.id})

        clinic_payment_record = self.env["clinic.payment"].search(
            [("name", "=", patient.id)]
        )
        if not clinic_payment_record:
            self.env["clinic.payment"].create({"name": patient.id})

        # Update the existing medical check record if it exists
        else:
            clinic_payment_record.write({"name": patient.id})

            # self.env["doctor.inspection"].create({"name": patient.id})

            # self.env["clinic.payment"].create({"name": patient.id})

        return patient

    # @api.depends("name")
    # def _compute_capitalized_name(self):
    #     for rec in self:
    #         if rec.name:
    #             rec.capitalized_name = rec.name.upper()
    #         else:
    #             rec.capitalized_name = ""

    # @api.onchange("age")
    # def _onchange_age(self):
    #     if self.age <= 10:
    #         self.is_child = True
    #     else:
    #         self.is_child = False

# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


# creating databased
class ClinicPayment(models.Model):
    _name = "clinic.payment"
    _inherit = ["mail.thread"]
    _description = "Clinic Payment"
    _rec_name = "ref"

    name = fields.Many2one(
        comodel_name="hospital.patient", string="Patient", required=True
    )
    ref = fields.Char(string="Reference", default=lambda self: _("New"))
    premed = fields.Many2one(
        comodel_name="medical.check",
        string="Pre Medical Record",
        domain="[('name', '=', name)]",
        # domain="[('check_date', '!=', False)]",
        # default=lambda self: self._default_latest_record,
    )
    record = fields.Many2one(
        comodel_name="doctor.inspection",
        string="Inspection Record",
        domain="[('name', '=', name)]",
        # domain="[('check_date', '!=', False)]",
        # default=lambda self: self._default_latest_record,
    )
    check_date = fields.Date(
        string="Check Date",
        default=fields.Date.today,
        related="record.check_date",
    )
    main_complaint = fields.Char(
        string="Main Complaint",
        tracking=True,
        related="premed.main_complaint",
    )
    interim_diagnosis = fields.Char(
        string="Interim Diagnosis",
        tracking=True,
        related="record.interim_diagnosis",
    )
    prescription = fields.Text(
        string="Prescription", tracking=True, related="record.prescription"
    )
    inspection_cost = fields.Float(
        string="Inspection Cost", related="record.total_cost"
    )

    # description = fields.Text(string="Description")
    # status = fields.Selection(
    #     [("todo", "To Do"), ("in_progress", "In Progress"), ("done", "Done")],
    #     string="Status",
    #     default="todo",
    # )

    @api.model
    def create(self, vals):
        # Generate the reference code if not provided
        if vals.get("ref", _("New")) == _("New"):
            vals["ref"] = self.env["ir.sequence"].next_by_code("clinic.payment") or _(
                "New"
            )

        # Create the DoctorInspection record
        payment = super(ClinicPayment, self).create(vals)

        # Update front office records
        self.update_payment(vals)

        return payment

    def write(self, vals):
        res = super(ClinicPayment, self).write(vals)
        if vals:
            frontoffice_record = self.env["clinic.frontoffice"].search(
                [("name", "=", self.name.id), ("status", "=", "payment")], limit=1
            )
            if frontoffice_record:
                frontoffice_record.write({"status": "done"})
        return res

    def update_payment(self, vals):
        payment_ref = self.env["clinic.frontoffice"].search(
            [("name", "=", vals.get("name"))]
        )
        payment_ref._compute_payment()

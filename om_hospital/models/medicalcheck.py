# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class MedicalCheck(models.Model):
    _name = "medical.check"
    _inherit = ["mail.thread"]
    _description = "Medical Checkup"
    _rec_name = "ref"

    name = fields.Many2one(
        comodel_name="hospital.patient", string="Patient", required=True
    )
    frontdesk = fields.Many2one(
        comodel_name="clinic.frontoffice",
        string="Front Desk Number",
        domain="[('name', '=', name)]",
    )
    status = fields.Selection(related="frontdesk.status", string="status")
    ref = fields.Char(string="Reference", default=lambda self: _("New"))

    # name = fields.Char(
    #     string="Patient", tracking=True, compute="_compute_capitalized_name", store=True
    # )
    # patient_id = fields.Many2one(
    #     comodel_name="hospital.patient", string="Patient", required=True
    # )
    check_date = fields.Date(string="Check Date", default=fields.Date.today)
    main_complaint = fields.Char(
        string="Main Complaint",
        tracking=True,
    )
    weight = fields.Float(string="Weight(Kg)", tracking=True)
    height = fields.Float(string="Height(Cm)", tracking=True)
    blood_pressure = fields.Float(string="Blood Pressure", tracking=True)
    spo2 = fields.Float(
        string="Oxygen saturation (SpO2)",
        tracking=True,
    )
    temperature = fields.Float(string="Temperature (°C)")

    def write(self, vals):
        result = super(MedicalCheck, self).write(vals)
        if self.frontdesk and self.frontdesk.status != "payment":
            # Change status to 'c' in related Form A if not already 'd'
            self.frontdesk.status = "docinspect"
        return result

    @api.model
    def create(self, vals):
        if vals.get("ref", _("New")) == _("New"):
            vals["ref"] = self.env["ir.sequence"].next_by_code("patient.premed") or _(
                "New"
            )

        premed = super(MedicalCheck, self).create(vals)
        self.update_foffice(vals)
        return premed

    def update_foffice(self, vals):
        foffice_records = self.env["clinic.frontoffice"].search(
            [("name", "=", vals.get("name"))]
        )
        foffice_records._compute_related_fields()

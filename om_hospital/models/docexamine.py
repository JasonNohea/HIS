# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


# creating databased
class DoctorInspection(models.Model):
    _name = "doctor.inspection"
    _inherit = ["mail.thread"]
    _description = "Doctor Inspection"

    name = fields.Char(
        string="Name", tracking=True, compute="_compute_capitalized_name", store=True
    )
    patient_id = fields.Many2one(
        comodel_name="hospital.patient", string="Patient", required=True
    )
    main_complaint = fields.Char(
        string="Main Complaint",
        tracking=True,
    )
    interim_diagnosis = fields.Char(
        string="Interim Diagnosis", tracking=True, required=True
    )
    additional_consult = fields.Char(
        string="Additional Referrals or Consultations", tracking=True
    )
    treatment_approach = fields.Char(
        string="Treatment Approach", tracking=True, required=True
    )
    additional_note = fields.Text(
        string="Additional Notes or Doctor's Observations", tracking=True
    )
    action = fields.Many2many("clinic.action", string="Action")
    equipment = fields.Many2many("clinic.equipment", string="Equipment & Supply")

    @api.depends("patient_id.name")
    def _compute_capitalized_name(self):
        for rec in self:
            if rec.patient_id:
                rec.name = rec.patient_id.name.upper()
            else:
                rec.name = ""

# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


# creating databased
class DoctorExamination(models.Model):
    _name = "doctor.examination"
    _inherit = ["mail.thread"]
    _description = "Doctor Examination"

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

    @api.depends("patient_id.name")
    def _compute_capitalized_name(self):
        for rec in self:
            if rec.patient_id:
                rec.name = rec.patient_id.name.upper()
            else:
                rec.name = ""

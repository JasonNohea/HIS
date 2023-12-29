# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class MedicalCheck(models.Model):
    _name = "medical.check"
    _inherit = ["mail.thread"]
    _description = "Medical Checkup"

    name = fields.Char(
        string="Name", tracking=True, compute="_compute_capitalized_name", store=True
    )
    patient_id = fields.Many2one(
        comodel_name="hospital.patient", string="Patient", required=True
    )
    check_date = fields.Date(string="Check Date", default=fields.Date.today)
    weight = fields.Float(string="Weight(Kg)", required=True, tracking=True)
    height = fields.Float(string="Height(Cm)", required=True, tracking=True)
    blood_pressure = fields.Float(string="Blood Pressure", required=True, tracking=True)
    spo2 = fields.Float(
        string="Saturasi Oksigen (SpO2)",
        required=True,
        tracking=True,
    )

    @api.depends("patient_id.name")
    def _compute_capitalized_name(self):
        for rec in self:
            if rec.patient_id:
                rec.name = rec.patient_id.name.upper()
            else:
                rec.name = ""

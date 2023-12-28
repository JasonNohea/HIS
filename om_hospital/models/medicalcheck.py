# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class MedicalCheck(models.Model):
    _name = "medical.check"
    _inherit = ["mail.thread"]
    _description = "Medical Checkup"

    name = fields.Char(string="Name", required=True, tracking=True)
    patient_id = fields.Many2one(
        comodel_name="hospital.patient", string="Patient", required=True
    )
    check_date = fields.Date(string="Check Date")

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
    ref = fields.Char(string="Reference", default=lambda self: _("New"))
    # name = fields.Char(
    #     string="Patient", tracking=True, compute="_compute_capitalized_name", store=True
    # )
    # patient_id = fields.Many2one(
    #     comodel_name="hospital.patient", string="Patient", required=True
    # )
    check_date = fields.Date(string="Check Date", default=fields.Date.today)
    weight = fields.Float(string="Weight(Kg)", required=True, tracking=True)
    height = fields.Float(string="Height(Cm)", required=True, tracking=True)
    blood_pressure = fields.Float(string="Blood Pressure", required=True, tracking=True)
    spo2 = fields.Float(
        string="Oxygen saturation (SpO2)",
        required=True,
        tracking=True,
    )
    temperature = fields.Float(string="Temperature (°C)")

    @api.model_create_multi
    def create(self, vals_list):
        # Modify the values in each dictionary
        for vals in vals_list:
            vals["ref"] = self.env["ir.sequence"].next_by_code("patient.premed")
            # vals["gender"] = "female"
        return super(MedicalCheck, self).create(vals_list)

    # @api.depends("patient_id.name")
    # def _compute_capitalized_name(self):
    #     for rec in self:
    #         if rec.patient_id:
    #             rec.name = rec.patient_id.name.upper()
    #         else:
    #             rec.name = ""

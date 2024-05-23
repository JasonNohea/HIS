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
        comodel_name="clinic.frontoffice", string="Front Desk Number"
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

    # @api.model_create_multi
    # def create(self, vals_list):
    #     # Modify the values in each dictionary
    #     for vals in vals_list:
    #         vals["ref"] = self.env["ir.sequence"].next_by_code("patient.premed")
    #         # vals["gender"] = "female"
    #     return super(MedicalCheck, self).create(vals_list)

    # def write(self, vals):
    #     res = super(MedicalCheck, self).write(vals)
    #     if vals:
    #         frontoffice_record = self.env["clinic.frontoffice"].search(
    #             [("premed", "=", self.id)], limit=1
    #         )
    #         if frontoffice_record:
    #             frontoffice_record.write({"status": "docinspect"})
    # return res

    # @api.depends("name")
    # def _get_frontoffice(self):
    #     for foffice in self:
    #         frontoffice = self.env["clinic.frontoffice"].search(
    #             [("name", "=", foffice.name.id)], limit=1
    #         )
    #         if frontoffice:
    #             foffice.frontdesk = frontoffice.id
    #         else:
    #             foffice.frontdesk = False

    @api.model
    def create(self, vals):
        if vals.get("ref", _("New")) == _("New"):
            vals["ref"] = self.env["ir.sequence"].next_by_code("patient.premed") or _(
                "New"
            )

        premed = super(MedicalCheck, self).create(vals)

        self.update_foffice(vals)

        # Automatically create a premed in clinic.frontoffice
        # self.env["clinic.frontoffice"].create(
        #     {"name": premed.name.id, "premed": premed.id, "status": "frontdesk"}
        # )

        # self.env["doctor.inspection"].create({"name": premed.name.id})
        # self.env["clinic.payment"].create(
        #     {
        #         "name": premed.name.id,
        #         "premed": premed.id,
        #     }
        # )

        return premed

    # @api.depends("patient_id.name")
    # def _compute_capitalized_name(self):
    #     for rec in self:
    #         if rec.patient_id:
    #             rec.name = rec.patient_id.name.upper()
    #         else:
    #             rec.name = ""

    def update_foffice(self, vals):
        foffice_records = self.env["clinic.frontoffice"].search(
            [("name", "=", vals.get("name"))]
        )
        foffice_records._compute_premed()

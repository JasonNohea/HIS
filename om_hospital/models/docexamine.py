# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


# creating databased
class DoctorInspection(models.Model):
    _name = "doctor.inspection"
    _inherit = ["mail.thread"]
    _description = "Doctor Inspection"

    name = fields.Many2one(
        comodel_name="hospital.patient", string="Patient", required=True
    )
    ref = fields.Char(string="Reference", default=lambda self: _("New"))
    doctor_assigned = fields.Many2one(
        comodel_name="clinic.doctor", string="Doctor Assigned", required=True
    )
    nurse_assigned = fields.Many2one(
        comodel_name="clinic.nurse", string="Nurse Assigned", required=True
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
    # treatment_approach = fields.Char(
    #     string="Treatment Approach", tracking=True, required=True
    # )
    additional_note = fields.Text(
        string="Additional Notes or Doctor's Observations", tracking=True
    )
    action = fields.Many2many("clinic.action", string="Action")
    display = fields.Char(string="Display", compute="_display", store=True)
    equipment = fields.Many2many("clinic.equipment", string="Equipment & Supply")
    action_cost = fields.Float(string="Action Cost", compute="_compute_action_cost")
    equipment_cost = fields.Float(
        string="Supply Cost", compute="_compute_equipment_cost"
    )
    total_cost = fields.Float(string="Total Cost", compute="_compute_total_cost")

    # @api.depends("patient_id.name")
    # def _compute_capitalized_name(self):
    #     for rec in self:
    #         if rec.patient_id:
    #             rec.name = rec.patient_id.name.upper()
    #         else:
    #             rec.name = ""

    @api.depends("action")
    def _display(self):
        for record in self:
            display_str = ", ".join(record.action.mapped("name"))
            record.display = display_str

    @api.depends("action.cost")
    def _compute_action_cost(self):
        for check in self:
            action_cost = sum(check.action.mapped("cost"))
            check.action_cost = action_cost

    @api.depends("equipment.cost")
    def _compute_equipment_cost(self):
        for check in self:
            equipment_cost = sum(check.equipment.mapped("cost"))
            check.equipment_cost = equipment_cost

    @api.depends("action_cost", "equipment_cost")
    def _compute_total_cost(self):
        for check in self:
            check.total_cost = check.action_cost + check.equipment_cost

    @api.model_create_multi
    def create(self, vals_list):
        # Modify the values in each dictionary
        for vals in vals_list:
            vals["ref"] = self.env["ir.sequence"].next_by_code("doctor.inspection")
            # vals["gender"] = "female"
        return super(DoctorInspection, self).create(vals_list)

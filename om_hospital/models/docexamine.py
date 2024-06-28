# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


# creating databased
class DoctorInspection(models.Model):
    _name = "doctor.inspection"
    _inherit = ["mail.thread"]
    _description = "Doctor Inspection"
    _rec_name = "ref"

    name = fields.Many2one(
        comodel_name="hospital.patient", string="Patient", required=True
    )
    ref = fields.Char(string="Reference", default=lambda self: _("New"))
    frontdesk = fields.Many2one(
        comodel_name="clinic.frontoffice",
        string="Front Desk Number",
        domain="[('name', '=', name)]",
    )

    doctor_assigned = fields.Many2one(
        related="frontdesk.doctor_assigned",
        string="Doctor Assigned",
        # domain=[("status", "=", "standby")],
    )

    status = fields.Selection(related="frontdesk.status", string="status")
    check_date = fields.Date(string="Check Date", default=fields.Date.today)

    interim_diagnosis = fields.Char(
        string="Interim Diagnosis",
        tracking=True,
    )
    additional_consult = fields.Char(
        string="Additional Referrals or Consultations", tracking=True
    )
    prescription = fields.Text(string="Prescription", tracking=True)
    additional_note = fields.Text(
        string="Additional Notes or Doctor's Observations", tracking=True
    )
    action = fields.Many2many("clinic.action", string="Action")
    display = fields.Char(string="Display", compute="_display", store=True)
    equipment_usage_ids = fields.One2many(
        "equipment.usage", "inspection_id", string="Equipment Lines"
    )
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

    def write(self, vals):
        result = super(DoctorInspection, self).write(vals)
        if self.frontdesk and self.frontdesk.status != "done":
            # Change status to 'c' in related Form A if not already 'd'
            self.frontdesk.status = "payment"
        return result

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

    @api.depends("equipment_usage_ids.total_cost")
    def _compute_equipment_cost(self):
        for inspection in self:
            total_cost = sum(
                usage.total_cost for usage in inspection.equipment_usage_ids
            )
            inspection.equipment_cost = total_cost

    # @api.depends("equipment.cost")
    # def _compute_equipment_cost(self):
    #     for check in self:
    #         equipment_cost = sum(check.equipment.mapped("cost"))
    #         check.equipment_cost = equipment_cost

    @api.depends("action_cost", "equipment_cost")
    def _compute_total_cost(self):
        for check in self:
            check.total_cost = check.action_cost + check.equipment_cost

    # @api.model_create_multi
    # def create(self, vals):
    #     if vals.get("ref", _("New")) == _("New"):
    #         vals["ref"] = self.env["ir.sequence"].next_by_code(
    #             "patient.inspection"
    #         ) or _("New")

    #     record = super(DoctorInspection, self).create(vals)

    #     # Automatically create a record in clinic.frontoffice
    #     self.env["clinic.frontoffice"].create({"record": record.id})

    #     return record

    @api.model
    def create(self, vals):
        if vals.get("ref", _("New")) == _("New"):
            vals["ref"] = self.env["ir.sequence"].next_by_code(
                "patient.inspection"
            ) or _("New")

        record = super(DoctorInspection, self).create(vals)
        self.update_foffice(vals)
        return record

    def update_foffice(self, vals):
        foffice_records = self.env["clinic.frontoffice"].search(
            [("name", "=", vals.get("name"))]
        )
        foffice_records._compute_related_fields()

    def _update_equipment_stock(self, usage_record):
        equipment = usage_record.name
        equipment_stock = equipment.stock - usage_record.quantity
        equipment.write({"stock": equipment_stock})

    # def create(self, vals):
    #     record = super(DoctorInspection, self).create(vals)
    #     # Call method to update records in Form A
    #     self.update_foffice(vals)
    #     return record

    def action_open_payment_record(self):
        payment = self.env["clinic.payment"].search(
            [("name", "=", self.name.id)], limit=1
        )
        if payment:
            return {
                "type": "ir.actions.act_window",
                "res_model": "clinic.payment",
                "view_mode": "form",
                "res_id": payment.id,
                "target": "current",
            }
        else:
            return {
                "type": "ir.actions.act_window",
                "res_model": "clinic.payment",
                "view_mode": "form",
                "target": "current",
                "context": {"default_name": self.name.id},
            }

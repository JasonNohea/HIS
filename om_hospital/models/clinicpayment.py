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
    frontdesk = fields.Many2one(
        comodel_name="clinic.frontoffice",
        string="Front Desk Number",
        domain="[('name', '=', name)]",
    )
    premed = fields.Many2one(
        comodel_name="medical.check",
        string="Pre Medical Record",
        related="frontdesk.premed",
        # domain="[('check_date', '!=', False)]",
        # default=lambda self: self._default_latest_record,
    )
    record = fields.Many2one(
        comodel_name="doctor.inspection",
        string="Inspection Record",
        related="frontdesk.record",
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

    action = fields.Many2many(
        comodel_name="clinic.action",
        string="Action",
        compute="_compute_action",
        store=False,
    )
    action_cost = fields.Float(
        string="Action Cost", compute="_compute_action_cost", store=False
    )

    equipment_usage_ids = fields.One2many(
        comodel_name="equipment.usage",
        inverse_name="inspection_id",
        string="Equipment Usage",
        compute="_compute_equipment_usage_ids",
        store=False,
    )

    payment_done = fields.Boolean(string="Payment Done", tracking=True)
    # description = fields.Text(string="Description")
    # status = fields.Selection(
    #     [("todo", "To Do"), ("in_progress", "In Progress"), ("done", "Done")],
    #     string="Status",
    #     default="todo",
    # )

    def write(self, vals):
        result = super(ClinicPayment, self).write(vals)
        if self.frontdesk:
            # Change status to 'd' in related Form A
            self.frontdesk.status = "done"
        return result

    @api.model
    def create(self, vals):
        if vals.get("ref", _("New")) == _("New"):
            vals["ref"] = self.env["ir.sequence"].next_by_code("clinic.payment") or _(
                "New"
            )

        record = super(ClinicPayment, self).create(vals)
        self.update_foffice(vals)
        return record

    def update_foffice(self, vals):
        foffice_records = self.env["clinic.frontoffice"].search(
            [("name", "=", vals.get("name"))]
        )
        foffice_records._compute_related_fields()

    @api.depends("record.equipment_usage_ids")
    def _compute_equipment_usage_ids(self):
        for payment in self:
            if payment.record:
                payment.equipment_usage_ids = payment.record.equipment_usage_ids
            else:
                payment.equipment_usage_ids = self.env["equipment.usage"]

    @api.depends("record.action")
    def _compute_action(self):
        for payment in self:
            if payment.record:
                payment.action = payment.record.action
            else:
                payment.action = self.env["clinic.action"]

    @api.depends("record.action_cost")
    def _compute_action_cost(self):
        for payment in self:
            if payment.record:
                payment.action_cost = payment.record.action_cost
            else:
                payment.action_cost = 0

    def action_save(self):
        # Additional logic to be executed before saving, if any
        self.ensure_one()
        self.write({})

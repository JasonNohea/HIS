# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


# creating databased
class ClinicServices(models.Model):
    _name = "clinic.payment"
    _inherit = ["mail.thread"]
    _description = "Clinic Payment"

    name = fields.Many2one(
        comodel_name="hospital.patient", string="Patient", required=True
    )
    premed = fields.Many2one(
        comodel_name="medical.check",
        string="Pre Medical Record",
        domain="[('name', '=', name)]",
        # domain="[('check_date', '!=', False)]",
        # default=lambda self: self._default_latest_record,
    )
    record = fields.Many2one(
        comodel_name="doctor.inspection",
        string="Inspection Record",
        domain="[('name', '=', name)]",
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

    # description = fields.Text(string="Description")
    # status = fields.Selection(
    #     [("todo", "To Do"), ("in_progress", "In Progress"), ("done", "Done")],
    #     string="Status",
    #     default="todo",
    # )

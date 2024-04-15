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
    description = fields.Text(string="Description")
    status = fields.Selection(
        [("todo", "To Do"), ("in_progress", "In Progress"), ("done", "Done")],
        string="Status",
        default="todo",
    )

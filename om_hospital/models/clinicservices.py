# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


# creating databased
class ClinicServices(models.Model):
    _name = "clinic.services"
    _inherit = ["mail.thread"]
    _description = "Clinic Services"

    name = fields.Char(
        string="Name", tracking=True, compute="_fetch_service", store=True
    )
    service = fields.Char(string="Service", required=True, tracking=True)
    description = fields.Text(string="Description")
    status = fields.Selection(
        [("todo", "To Do"), ("in_progress", "In Progress"), ("done", "Done")],
        string="Status",
        default="todo",
    )

    @api.depends("service")
    def _fetch_service(self):
        for rec in self:
            if rec.service:
                rec.name = rec.service
            else:
                rec.name = ""

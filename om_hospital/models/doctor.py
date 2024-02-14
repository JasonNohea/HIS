# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


# creating databased
class ClinicDoctor(models.Model):
    _name = "clinic.doctor"
    _inherit = ["mail.thread"]
    _description = "Clinic Doctor"

    name = fields.Char(string="Name", tracking=True, store=True)
    photo = fields.Binary(string="Photo")
    specialization = fields.Char(string="Specialization", required=True, tracking=True)
    description = fields.Text(string="Description")
    status = fields.Selection(
        [("working", "working"), ("standby", "On Standby")],
        string="Status",
        default="standby",
        required=True,
    )

    # @api.depends("service")
    # def _fetch_service(self):
    #     for rec in self:
    #         if rec.service:
    #             rec.name = rec.service
    #         else:
    #             rec.name = ""

# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class DoctorCheck(models.Model):
    _name = "doctor.check"
    _inherit = ["mail.thread"]
    _description = "Doctor Checkup"

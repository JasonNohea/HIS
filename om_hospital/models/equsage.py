# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


# creating databased
class EquipmentUsage(models.Model):
    _name = "equipment.usage"
    _inherit = ["mail.thread"]
    _description = "Equipment Usage"

    name = fields.Many2one("clinic.equipment", string="Equipment")
    inspection_id = fields.Many2one("doctor.inspection", string="Inspection")
    equipment_id = fields.Many2one("clinic.equipment", string="Equipment")
    quantity = fields.Integer(string="Quantity")

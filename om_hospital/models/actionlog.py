# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


# creating databased
class ActionLog(models.Model):
    _name = "action.log"
    _inherit = ["mail.thread"]
    _description = "Action Log"

    name = fields.Many2one("clinic.action", string="Equipment")
    inspection_id = fields.Many2one("doctor.inspection", string="Inspection")
    # equipment_id = fields.Many2one("clinic.equipment", string="Equipment")
    # quantity = fields.Integer(string="Quantity")
    notes = fields.Text(string="Doctor Notes")
    usage_cost = fields.Float(string="Usage Cost", related="name.cost")
    # total_cost = fields.Float(string="Total Cost", compute="_compute_total_cost")

    @api.model
    def create(self, vals):
        record = super(ActionLog, self).create(vals)
        return record

    def write(self, vals):
        res = super(ActionLog, self).write(vals)
        return res

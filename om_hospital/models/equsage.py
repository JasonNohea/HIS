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
    # equipment_id = fields.Many2one("clinic.equipment", string="Equipment")
    quantity = fields.Integer(string="Quantity")
    usage_cost = fields.Float(string="Usage Cost", related="name.cost")
    total_cost = fields.Float(string="Total Cost", compute="_compute_total_cost")

    @api.depends("quantity", "usage_cost")
    def _compute_total_cost(self):
        for record in self:
            record.total_cost = record.quantity * record.usage_cost

    @api.model
    def create(self, vals):
        record = super(EquipmentUsage, self).create(vals)
        record.update_equipment_stock()
        return record

    def write(self, vals):
        res = super(EquipmentUsage, self).write(vals)
        self.update_equipment_stock()
        return res

    def update_equipment_stock(self):
        for usage in self:
            usage.name.stock -= usage.quantity

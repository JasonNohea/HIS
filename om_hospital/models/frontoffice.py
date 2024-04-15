from odoo import models, fields, api


class nurse(models.Model):
    _name = "clinic.frontoffice"
    _inherit = ["mail.thread"]
    _description = "Clinic Front Office"

    name = name = fields.Many2one(
        comodel_name="hospital.patient", string="Patient", required=True
    )
    room_assigned = fields.Many2one(
        comodel_name="clinic.rooms", string="Rooms Assigned", required=True
    )
    cost = fields.Many2one(
        comodel_name="doctor.inspection", string="Cost", required=True
    )
    description = fields.Text(string="Description")

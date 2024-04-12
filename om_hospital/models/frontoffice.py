from odoo import models, fields, api


class nurse(models.Model):
    _name = "clinic.frontoffice"
    _inherit = ["mail.thread"]
    _description = "Clinic Front Office"

    name = fields.Char(string="Name")
    cost = fields.Float(string="Cost")
    description = fields.Text(string="Description")

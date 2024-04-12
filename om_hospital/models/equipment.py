from odoo import models, fields, api


class nurse(models.Model):
    _name = "clinic.equipment"
    _inherit = ["mail.thread"]
    _description = "Clinic Equipment & Supply"

    name = fields.Char(string="Name")
    stock = fields.Integer(string="Stock")
    cost = fields.Float(string="Cost")
    type = fields.Selection(
        [
            ("supply", "Supply"),
            ("Equipment", "Equipment"),
        ],
        string="Type",
        default="",
        required=True,
    )
    provider = fields.Char(string="Manufacturer/Supplier")
    description = fields.Text(string="Description")
    status = fields.Selection(
        [
            ("operational", "Operational"),
            ("maintenance", "Under Maintenance"),
            ("outofservice", "Out of Service"),
            ("available", "Available"),
            ("needrestock", "Restock Needed"),
        ],
        string="Status",
        default="",
        required=True,
    )

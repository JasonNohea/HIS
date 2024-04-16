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
    order = fields.Many2one(
        comodel_name="doctor.inspection",
        string="Patient Order",
        domain=lambda self: [("field_name", "=", "value")],
        default=lambda self: self._default_latest_record,
    )
    description = fields.Text(string="Description")

    def _default_latest_record(self):
        latest_record = self.env["doctor.inspection"].search(
            [], order="date_field DESC", limit=1
        )
        return latest_record.id if latest_record else False

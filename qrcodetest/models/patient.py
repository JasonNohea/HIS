import qrcode
from io import BytesIO
from odoo import models, fields, api


class Patient(models.Model):
    _name = "patient.model"
    _inherit = ["mail.thread"]
    _description = "Patient Records"

    name = fields.Char(string="Name")
    ref_code = fields.Char(string="Reference Code", readonly=True)
    qr_code_image = fields.Binary(string="QR Code", compute="_generate_qr_code")

    @api.model
    def create(self, vals):
        vals["ref_code"] = self.env["ir.sequence"].next_by_code("patient.ref") or "/"
        return super(Patient, self).create(vals)

    @api.depends("ref_code")
    def _generate_qr_code(self):
        for patient in self:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(patient.ref_code)
            qr.make(fit=True)

            img = qr.make_image(fill_color="black", back_color="white")
            buffered = BytesIO()
            img.save(buffered, format="PNG")
            patient.qr_code_image = buffered.getvalue()

from odoo import models, fields, api


class testfield(models.Model):
    _name = "testfield.model"
    _inherit = ["mail.thread"]
    _description = "TestField"

    name = fields.Char(string="Name")
    ref_code = fields.Char(string="Reference Code", readonly=True)
    choose = fields.Selection([("yes", "Yes"), ("no", "No")], string="Combo Box Field")
    field = fields.Char(string="Editable Field", readonly=True)
    file = fields.Binary(string="File")

    @api.onchange("choose")
    def _onchange_choose(self):
        if self.choose == "yes":
            self.field = False
        elif self.choose == "no":
            self.field = True

    @api.model
    def create(self, vals):
        vals["ref_code"] = self.env["ir.sequence"].next_by_code("TestField.ref") or "/"
        return super(testfield, self).create(vals)

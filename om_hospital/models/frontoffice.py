import logging
from odoo import models, fields, api, _
from contextlib import contextmanager

# Set up logging
_logger = logging.getLogger(__name__)


class FrontOffice(models.Model):
    _name = "clinic.frontoffice"
    _inherit = ["mail.thread"]
    _description = "Clinic Front Office"
    _rec_name = "ref"

    name = fields.Many2one(
        comodel_name="hospital.patient",
        string="Patient",
    )
    ref = fields.Char(string="Reference", default=lambda self: _("New"))
    premed = fields.Many2one(
        comodel_name="medical.check",
        string="Pre Medical Record",
        domain="[('name', '=', name)]",
        # domain="[('check_date', '!=', False)]",
        # default=lambda self: self._default_latest_record,
    )

    record = fields.Many2one(
        comodel_name="doctor.inspection",
        string="Inspection Record",
        domain="[('name', '=', name)]",
        # domain="[('check_date', '!=', False)]",
        # default=lambda self: self._default_latest_record,
    )

    payment = fields.Many2one(
        comodel_name="clinic.payment",
        string="Payment",
        domain="[('name', '=', name)]",
        # domain="[('check_date', '!=', False)]",
        # default=lambda self: self._default_latest_record,
    )

    status = fields.Selection(
        [
            # ("notcheck", "Awaiting Check-in"),
            ("frontdesk", "Checking in at Front Desk"),
            ("premed", "Ready for Premedical Check"),
            ("docinspect", "Ready for Doctor Inspection"),
            ("payment", "In Payment Processing"),
            ("done", "Payment Process Completed"),
        ],
        string="Status",
        default="frontdesk",
    )

    date_of_birth = fields.Date(
        string="Date of Birth",
        default=False,
        related="name.date_of_birth",
        # default=lambda self: fields.Date.today(),
        # Add a domain to restrict the date range
        # domain="[('date', '<=', fields.Date.today())]",
    )
    daycount = fields.Char(
        string="Day",
        tracking=True,
        related="name.daycount",
    )
    monthcount = fields.Char(
        string="Month",
        tracking=True,
        related="name.monthcount",
    )
    yearcount = fields.Char(
        string="Year",
        tracking=True,
        related="name.yearcount",
    )

    gender = fields.Selection(
        [("male", "Male"), ("female", "Female"), ("others", "Others")],
        string="Gender",
        tracking=True,
        related="name.gender",
    )
    bloodtype = fields.Selection(
        [
            ("A+", "A+"),
            ("B+", "B+"),
            ("O+", "O+"),
            ("AB+", "AB+"),
            ("A-", "A-"),
            ("B-", "B-"),
            ("O-", "O-"),
            ("AB-", "AB-"),
        ],
        string="Blood Type",
        related="name.bloodtype",
        tracking=True,
    )

    check_date = fields.Date(
        string="Check Date", related="premed.check_date", tracking=True
    )
    weight = fields.Float(string="Weight(Kg)", related="premed.weight", tracking=True)
    height = fields.Float(string="Height(Cm)", related="premed.height", tracking=True)
    blood_pressure = fields.Float(
        string="Blood Pressure", related="premed.blood_pressure", tracking=True
    )
    spo2 = fields.Float(
        string="Oxygen saturation (SpO2)",
        related="premed.spo2",
        tracking=True,
    )
    temperature = fields.Float(string="Temperature (°C)", related="premed.temperature")

    room_assigned = fields.Many2one(
        comodel_name="clinic.rooms",
        string="Rooms Assigned",
    )

    doctor_assigned = fields.Many2one(
        comodel_name="clinic.doctor",
        string="Doctor Assigned",
    )

    nurse_assigned = fields.Many2one(
        comodel_name="clinic.nurse",
        string="Nurse Assigned",
    )

    main_complaint = fields.Char(
        string="Main Complaint",
        tracking=True,
        related="premed.main_complaint",
    )
    interim_diagnosis = fields.Char(
        string="Interim Diagnosis",
        tracking=True,
        related="record.interim_diagnosis",
    )

    prescription = fields.Text(
        string="Prescription", tracking=True, related="record.prescription"
    )

    _skip_status_update = fields.Boolean(
        string="Skip Status Update", default=False, store=False
    )

    @api.model
    def create(self, vals):
        if vals.get("ref", _("New")) == _("New"):
            vals["ref"] = self.env["ir.sequence"].next_by_code("clinic.frontdesk") or _(
                "New"
            )

        foffice = super(FrontOffice, self).create(vals)

        patient_id = foffice.name.id

        self.env["medical.check"].create({"name": patient_id, "frontdesk": foffice.id})
        self.env["doctor.inspection"].create(
            {"name": patient_id, "frontdesk": foffice.id}
        )
        self.env["clinic.payment"].create({"name": patient_id, "frontdesk": foffice.id})

        # premed = self.env["medical.check"].search([("name", "=", patient_id)], limit=1)
        # if premed:
        #     premed.write({"frontdesk": foffice.id})

    @api.depends("name")
    def _compute_related_fields(self):
        for record in self:
            record.premed = (
                self.env["medical.check"]
                .search([("name", "=", record.name.id)], limit=1)
                .id
            )
            record.record = (
                self.env["doctor.inspection"]
                .search([("name", "=", record.name.id)], limit=1)
                .id
            )
            record.payment = (
                self.env["clinic.payment"]
                .search([("name", "=", record.name.id)], limit=1)
                .id
            )

    def write(self, vals):
        if "status" not in vals:
            # Change status to 'b' only if not already changed to 'c' or 'd'
            if self.status == "frontdesk":
                vals["status"] = "premed"
        return super(FrontOffice, self).write(vals)

    def _update_status(self, new_status):
        self.status = new_status
        _logger.info(f"Status updated to {new_status}")

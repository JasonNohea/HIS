from odoo import models, fields, api, _


class frontoffice(models.Model):
    _name = "clinic.frontoffice"
    _inherit = ["mail.thread"]
    _description = "Clinic Front Office"

    name = name = fields.Many2one(
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

    status = fields.Selection(
        [
            # ("notcheck", "Awaiting Check-in"),
            ("frontdesk", "Checking in at Front Desk"),
            ("premed", "Undergoing Pre-Medical Check"),
            ("docinspect", "Currently with Doctor for Inspection"),
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

    # room_assigned = fields.Many2one(
    #     comodel_name="clinic.rooms",
    #     string="Rooms Assigned",
    #     related="record.room_assigned",
    # )

    # doctor_assigned = fields.Many2one(
    #     comodel_name="clinic.doctor",
    #     string="Doctor Assigned",
    #     related="record.doctor_assigned",
    # )

    # nurse_assigned = fields.Many2one(
    #     comodel_name="clinic.nurse",
    #     string="Nurse Assigned",
    #     related="record.nurse_assigned",
    # )

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

    @api.model_create_multi
    def create(self, vals_list):
        # Modify the values in each dictionary
        for vals in vals_list:
            vals["ref"] = self.env["ir.sequence"].next_by_code("clinic.frontdesk")
            # vals["gender"] = "female"
        return super(frontoffice, self).create(vals_list)

    # description = fields.Text(string="Description")

    # def _default_latest_record(self):
    #     latest_record = self.env["doctor.inspection"].search(
    #         [], order="check_date DESC", limit=1
    #     )
    #     return latest_record.id if latest_record else False

from odoo import models, fields, api


class Equipment(models.Model):
    _name = "clinic.equipment"
    _inherit = ["mail.thread"]
    _description = "Clinic Equipment & Supply"

    name = fields.Char(string="Name", tracking=True)
    stock = fields.Integer(string="Stock", tracking=True)
    cost = fields.Float(string="Usage Cost", tracking=True)
    type = fields.Selection(
        [
            ("supply", "Supply"),
            ("equipment", "Equipment"),
        ],
        string="Type",
        default="",
        tracking=True,
    )
    provider = fields.Char(string="Manufacturer/Supplier", tracking=True)
    description = fields.Text(string="Description", tracking=True)
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
        tracking=True,
    )

    @api.model
    def create_predefined_equipment(self):
        predefined_equipment = [
            {
                "name": "Stethoscope",
                "stock": 20,
                "cost": 15.0,
                "type": "equipment",
                "provider": "Medical Supplies Inc.",
                "description": "Used for listening to internal sounds of a body.",
                "status": "operational",
            },
            {
                "name": "X-Ray Machine",
                "stock": 2,
                "cost": 100.0,
                "type": "equipment",
                "provider": "Radiology Experts Ltd.",
                "description": "Used for taking X-ray images.",
                "status": "maintenance",
            },
            {
                "name": "Syringe",
                "stock": 100,
                "cost": 1.0,
                "type": "equipment",
                "provider": "MedTech Co.",
                "description": "Used for injections.",
                "status": "needrestock",
            },
            {
                "name": "Scalpel",
                "stock": 50,
                "cost": 5.0,
                "type": "equipment",
                "provider": "Surgical Instruments Ltd.",
                "description": "Used for surgeries.",
                "status": "needrestock",
            },
            {
                "name": "Cotton",
                "stock": 500,
                "cost": 0.1,
                "type": "supply",
                "provider": "Health Supplies Inc.",
                "description": "Used for wound care.",
                "status": "needrestock",
            },
            {
                "name": "Bandage",
                "stock": 300,
                "cost": 0.5,
                "type": "supply",
                "provider": "Health Supplies Inc.",
                "description": "Used for dressing wounds.",
                "status": "needrestock",
            },
            {
                "name": "Blood Pressure Monitor",
                "stock": 10,
                "cost": 20.0,
                "type": "equipment",
                "provider": "Medical Devices Co.",
                "description": "Used to measure blood pressure.",
                "status": "operational",
            },
            {
                "name": "Thermometer",
                "stock": 25,
                "cost": 5.0,
                "type": "equipment",
                "provider": "Health Gadgets Ltd.",
                "description": "Used to measure body temperature.",
                "status": "operational",
            },
            {
                "name": "Ultrasound Machine",
                "stock": 1,
                "cost": 200.0,
                "type": "equipment",
                "provider": "Imaging Technologies Inc.",
                "description": "Used for ultrasound imaging.",
                "status": "maintenance",
            },
            {
                "name": "Gauze",
                "stock": 400,
                "cost": 0.2,
                "type": "supply",
                "provider": "MedSupply Co.",
                "description": "Used for wound care.",
                "status": "needrestock",
            },
            {
                "name": "IV Drip",
                "stock": 30,
                "cost": 10.0,
                "type": "equipment",
                "provider": "Medical Solutions Ltd.",
                "description": "Used for intravenous therapy.",
                "status": "available",
            },
            {
                "name": "Defibrillator",
                "stock": 3,
                "cost": 150.0,
                "type": "equipment",
                "provider": "CardioTech Inc.",
                "description": "Used for emergency heart treatments.",
                "status": "operational",
            },
            {
                "name": "Oxygen Tank",
                "stock": 15,
                "cost": 25.0,
                "type": "equipment",
                "provider": "OxyHealth Ltd.",
                "description": "Used to supply oxygen.",
                "status": "available",
            },
            {
                "name": "ECG Machine",
                "stock": 4,
                "cost": 75.0,
                "type": "equipment",
                "provider": "CardioTech Inc.",
                "description": "Used for electrocardiography.",
                "status": "operational",
            },
            {
                "name": "Gloves",
                "stock": 1000,
                "cost": 0.1,
                "type": "supply",
                "provider": "Health Supplies Inc.",
                "description": "Used for hygiene.",
                "status": "needrestock",
            },
            {
                "name": "Face Mask",
                "stock": 500,
                "cost": 0.2,
                "type": "supply",
                "provider": "Health Supplies Inc.",
                "description": "Used for hygiene.",
                "status": "needrestock",
            },
            {
                "name": "Hand Sanitizer",
                "stock": 200,
                "cost": 3.0,
                "type": "supply",
                "provider": "Health Supplies Inc.",
                "description": "Used for hygiene.",
                "status": "needrestock",
            },
            {
                "name": "Surgical Lamp",
                "stock": 5,
                "cost": 120.0,
                "type": "equipment",
                "provider": "Surgical Instruments Ltd.",
                "description": "Used for surgeries.",
                "status": "operational",
            },
            {
                "name": "Wheelchair",
                "stock": 8,
                "cost": 50.0,
                "type": "equipment",
                "provider": "Medical Devices Co.",
                "description": "Used for patient mobility.",
                "status": "operational",
            },
            {
                "name": "Crutches",
                "stock": 20,
                "cost": 15.0,
                "type": "equipment",
                "provider": "Medical Devices Co.",
                "description": "Used for patient mobility.",
                "status": "operational",
            },
        ]
        for equipment in predefined_equipment:
            self.create(equipment)

{
    "name": "Patient QR Code Generator",
    "version": "1.0",
    "category": "Tools",
    "summary": "Generates QR codes for patients in Odoo.",
    "description": """
        This module generates QR codes containing a reference code for patients in Odoo.
    """,
    "author": "QR Testing",
    "website": "https://www.example.com",
    "depends": ["mail", "web"],
    "data": [
        "security\ir.model.access.csv",
        "views\menu.xml",
        "views\patient.xml",
        "data\sequence.xml",
    ],
    "installable": True,
    "application": True,
}

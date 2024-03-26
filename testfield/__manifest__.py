{
    "name": "TestField",
    "version": "1.0",
    "category": "Tools",
    "summary": "TestField in Odoo.",
    "description": """
        This module will be used to test Odoo in anyway I want.
    """,
    "author": "TestOnly",
    "website": "https://www.example.com",
    "depends": ["mail", "web"],
    "data": [
        "security/ir.model.access.csv",
        "views/menu.xml",
        "views/testfield.xml",
        "data/sequence.xml",
    ],
    "installable": True,
    "application": True,
}

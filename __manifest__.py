{
    "name": "Odoo Trip Estimator",
    "description": """
    Odoo Trip Estimator
    This module is used to estimate the trip length and duration based on the distance between the source (our company) and the destination (contact).
    """,
    "author": "Louis Noël",
    "version": "0.1",
    "depends": ["base", "contacts", "base_geolocalize"],
    "installable": True,
    "application": True,
    "data": [
        "security/ir.model.access.csv",
        "views/res_partner.xml",
        "views/res_config_settings_views.xml",
    ],
}

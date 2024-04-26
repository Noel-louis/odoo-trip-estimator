{
    "name": "Odoo Trip Estimator",
    "summary": "Estimate the trip length and duration of you contacts.",
    "description": """
    Odoo Trip Estimator
    This module is used to estimate the trip length and duration based on the distance between the starting point and the destination (contact).
    """,
    "website": "https://github.com/Noel-louis/odoo_trip_estimator",
    "author": "Louis Noël",
    "version": "0.1",
    "depends": ["base", "contacts", "base_geolocalize"],
    "installable": True,
    "data": [
        "security/ir.model.access.csv",
        "views/res_partner.xml",
        "views/res_config_settings_views.xml",
    ],
}

from odoo import fields, models, _


class Geocode(models.Model):
    _name = "geocode"
    _description = "Geocode"

    x_tripestimator_latitude = fields.Float(string=_("Latitude"))
    x_tripestimator_longitude = fields.Float(string=_("Longitude"))
    x_tripestimator_address = fields.Char(string=_("Address"))

    def is_already_geolocalized(self, address):
        """Check if the address is already geolocalized in the database.

        Args:
            address (str): address to search in the database

        Returns:
            bool: True if the address is already geolocalized, False otherwise
        """
        geocode = self.search([("x_tripestimator_address", "=", address)])
        if geocode:
            return True
        else:
            return False

from odoo import api, fields, models, _


class Geocode(models.Model):
    _name = "geocode"
    _description = "Geocode"

    latitude = fields.Float(string=_("Latitude"))
    longitude = fields.Float(string=_("Longitude"))
    address = fields.Char(string=_("Address"))

    def is_already_geolocalized(self, address):
        geocode = self.search([("address", "=", address)])
        if geocode:
            return True
        else:
            return False

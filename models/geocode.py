from odoo import api, fields, models
from odoo.exceptions import UserError

import openrouteservice as ors
import openrouteservice.exceptions as ors_exc


class Geocode(models.Model):
    _name = "geocode"
    _description = "Geocode model for storing geocoding data"

    latitude = fields.Float(string="Latitude")
    longitude = fields.Float(string="Longitude")

    complete_address_inline = fields.Char(string="Complete Address Inline")

    def geocode_address(self, address):
        # search if the address is already geocoded
        geo = self.env["geocode"].search([("complete_address_inline", "=", address)])
        # verify if the address is not already geocoded
        if geo:
            return geo
        # create the client to interact with the OpenRouteService API
        token_api_key = self.env["ir.config_parameter"].get_param(
            "odoo-trip-estimator.key"
        )
        if not token_api_key:
            raise UserError("No API key found")
        client = ors.Client(key=token_api_key)
        # geocode the address and store the result in the geocode model instance and return it
        try:
            result = client.pelias_search(text=address)
            latitude = result["features"][0]["geometry"]["coordinates"][1]
            longitude = result["features"][0]["geometry"]["coordinates"][0]
            location = self.env["geocode"].create(
                {
                    "latitude": latitude,
                    "longitude": longitude,
                    "complete_address_inline": address,
                }
            )
            return location
        except ors_exc.ApiError as e:
            raise UserError(f"Error with the API: {e}")

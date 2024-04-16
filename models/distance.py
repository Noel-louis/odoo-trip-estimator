# _ is used to translate the string in the current language
from odoo import api, fields, models, _
from odoo.exceptions import UserError

import openrouteservice as ors
import openrouteservice.exceptions as ors_exc


class Distance(models.Model):
    _name = "distance"
    _description = "Distance model for storing distance data"

    # localisation of our entreprise
    latitude_1 = fields.Float(string="Latitude 1")
    longitude_1 = fields.Float(string="Longitude 1")

    # localisation of the contact
    latitude_2 = fields.Float(string="Latitude 2")
    longitude_2 = fields.Float(string="Longitude 2")

    # distance and transport time between our company and the contact (by car)
    distance = fields.Float(string="Distance")
    travel_time = fields.Float(string="Travel Time")

    def compute_distance(self, latitude_1, longitude_1, latitude_2, longitude_2):
        # search if the distance is already computed
        dist = self.env["distance"].search(
            [
                ("latitude_1", "=", latitude_1),
                ("longitude_1", "=", longitude_1),
                ("latitude_2", "=", latitude_2),
                ("longitude_2", "=", longitude_2),
            ]
        )
        if dist:
            return dist
        # create the client to interact with the OpenRouteService API
        token_api_key = self.env["ir.config_parameter"].get_param(
            "odoo-trip-estimator.key"
        )
        if not token_api_key:
            error_message = _("No API key found")
            raise UserError(error_message)
        client = ors.Client(key=token_api_key)
        try:
            direction = client.directions(
                coordinates=[[longitude_1, latitude_1], [longitude_2, latitude_2]],
                profile="driving-car",
            )
            result = self.env["distance"].create(
                {
                    "latitude_1": latitude_1,
                    "longitude_1": longitude_1,
                    "latitude_2": latitude_2,
                    "longitude_2": longitude_2,
                    "distance": direction["routes"][0]["summary"]["distance"],
                    "travel_time": direction["routes"][0]["summary"]["duration"],
                }
            )
            return result
        except ors_exc.ApiError as e:
            error_message = _("Error with the API: %s", e)
            raise UserError(error_message)

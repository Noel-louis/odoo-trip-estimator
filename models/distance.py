# _ is used to translate the string in the current language
from odoo import fields, models, _
from odoo.exceptions import UserError

import openrouteservice as ors
import openrouteservice.exceptions as ors_exc


class Distance(models.Model):
    _name = "distance"
    _description = "Distance model for storing distance data"

    # localisation of the starting point
    x_tripestimator_latitude_1 = fields.Float(string="Latitude 1")
    x_tripestimator_longitude_1 = fields.Float(string="Longitude 1")

    # localisation of the contact
    x_tripestimator_latitude_2 = fields.Float(string="Latitude 2")
    x_tripestimator_longitude_2 = fields.Float(string="Longitude 2")

    # distance and transport time between the starting point and the contact (by car)
    x_tripestimator_distance = fields.Float(string="Distance")
    x_tripestimator_travel_time = fields.Float(string="Travel Time")

    def compute_distance(self, latitude_1, longitude_1, latitude_2, longitude_2):
        # search if the distance is already computed
        dist = self.env["distance"].search(
            [
                ("x_tripestimator_latitude_1", "=", latitude_1),
                ("x_tripestimator_longitude_1", "=", longitude_1),
                ("x_tripestimator_latitude_2", "=", latitude_2),
                ("x_tripestimator_longitude_2", "=", longitude_2),
            ]
        )
        if dist:
            return dist
        # create the client to interact with the OpenRouteService API
        token_api_key = (
            self.env["ir.config_parameter"].sudo().get_param("odoo-trip-estimator.key")
        )
        if not token_api_key:
            error_message = _("No API key found")
            # we raise an error to inform the user that the API key is missing and the function will stop
            raise UserError(error_message)
        client = ors.Client(key=token_api_key)
        try:
            # call the API to get the distance and the travel time
            direction = client.directions(
                coordinates=[[longitude_1, latitude_1], [longitude_2, latitude_2]],
                profile="driving-car",
            )
            # Add the distance and the travel time in the database
            result = self.env["distance"].create(
                {
                    "x_tripestimator_latitude_1": latitude_1,
                    "x_tripestimator_longitude_1": longitude_1,
                    "x_tripestimator_latitude_2": latitude_2,
                    "x_tripestimator_longitude_2": longitude_2,
                    "x_tripestimator_distance": direction["routes"][0]["summary"][
                        "distance"
                    ],
                    "x_tripestimator_travel_time": direction["routes"][0]["summary"][
                        "duration"
                    ],
                }
            )
            return result
        except ors_exc.ApiError as e:
            # if there is an error with the API, we raise an error to inform the user
            error_message = _("Error with the API: %s", e)
            raise UserError(error_message)

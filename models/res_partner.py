# _ is used to translate the strings in the current language
from odoo import api, fields, models, _

import logging

_logger = logging.getLogger(__name__)


class res_partner(models.Model):
    _inherit = "res.partner"

    # starting point for the trip calculation
    x_tripestimator_contact_starting_point = fields.Many2one(
        "res.partner",
        string=_("Address Contact"),
        default=lambda self: self.env.company.partner_id.id,
    )
    x_tripestimator_contact_starting_points = fields.One2many(
        "res.partner",
        "x_tripestimator_contact_starting_point",
        string=_("Address Contact"),
    )

    # calcul data
    x_tripestimator_distance = fields.Float(string=_("Distance float"))
    x_tripestimator_time = fields.Float(string=_("Time float"))

    # printed data
    x_tripestimator_distance_char = fields.Char(
        string=_("Distance"), compute="_compute_distance_char"
    )
    x_tripestimator_time_char = fields.Char(
        string=_("Time"), compute="_compute_time_char"
    )

    @api.depends("x_tripestimator_contact_starting_points")
    def _compute_address_id(self):
        """Compute the address_id field to display the address in the view."""
        for record in self:
            if record.x_tripestimator_contact_starting_points:
                record.x_tripestimator_contact_starting_point = (
                    record.x_tripestimator_contact_starting_points[0].id
                )

    def _inverse_address_id(self):
        """Inverse the address_id field to update the address in the view."""
        for record in self:
            if record.x_tripestimator_contact_starting_point:
                record.x_tripestimator_contact_starting_points = [
                    (4, record.x_tripestimator_contact_starting_point.id)
                ]

    @api.depends("x_tripestimator_distance")
    def _compute_distance_char(self):
        """
        Prettify the distance field. If the distance is greater than 1000m, it will be displayed in km, otherwise in m.
        Just for the display, the value in the database is in meters and is x_tripestimator_distance.
        """
        for record in self:
            if record.x_tripestimator_distance > 1000:
                record.x_tripestimator_distance_char = "{:.1f} km".format(
                    (record.x_tripestimator_distance / 1000)
                )
            else:
                record.x_tripestimator_distance_char = (
                    str(record.x_tripestimator_distance) + " m"
                )

    @api.depends("x_tripestimator_time")
    def _compute_time_char(self):
        """
        Prettify the time field. If the time is greater than 60 minutes, it will be displayed in hours and minutes, otherwise in minutes.
        Just for the display, the value in the database is in minutes and is x_tripestimator_time.
        """
        for record in self:
            secondes = record.x_tripestimator_time % 60
            minutes = (record.x_tripestimator_time - secondes) / 60
            if minutes > 60:
                heures = (minutes - (minutes % 60)) / 60
                minutes = minutes % 60
                record.x_tripestimator_time_char = "{:.0f} h {:.0f} min".format(
                    heures, minutes
                )
            else:
                record.x_tripestimator_time_char = "{:.0f} min".format(minutes)

    def send_notification(self, message):
        """Send a notification to the user.

        Args:
            message (str): message to display in the notification
        """
        self.env["bus.bus"]._sendone(
            self.env.user.partner_id,
            "simple_notification",
            {"type": "warning", "title": _("Warning"), "message": message},
        )

    def calculate_distance(self):
        """Calculate the distance and the time between the contact and the starting point(default to company)."""
        same_address = False
        address_not_geolocalized = False
        contact_not_geolocalized = False
        for record in self:
            # geolocalize the addresses
            record.geo_localize()
            record.x_tripestimator_contact_starting_point.geo_localize()
            # check if the addresses are geolocalized and different
            if (
                record.partner_latitude
                == record.x_tripestimator_contact_starting_point.partner_latitude
                and record.partner_longitude
                == record.x_tripestimator_contact_starting_point.partner_longitude
            ):
                record.x_tripestimator_distance = 0
                record.x_tripestimator_time = 0
                same_address = True
            elif record.partner_latitude == 0 and record.partner_longitude == 0:
                address_not_geolocalized = True
            elif (
                record.x_tripestimator_contact_starting_point.partner_latitude == 0
                and record.x_tripestimator_contact_starting_point.partner_longitude == 0
            ):
                contact_not_geolocalized = True
            else:
                # compute the distance and the time
                dist = record.env["distance"].compute_distance(
                    record.partner_latitude,
                    record.partner_longitude,
                    record.x_tripestimator_contact_starting_point.partner_latitude,
                    record.x_tripestimator_contact_starting_point.partner_longitude,
                )
                # set the values of the fields
                record.x_tripestimator_distance = dist.x_tripestimator_distance
                record.x_tripestimator_time = dist.x_tripestimator_travel_time

        # check if there is one or more calculation to personnalize the notification
        if self.__len__() == 1:
            # send a notification if there is an error
            error_message = ""
            if address_not_geolocalized:
                error_message = _("The address of the contact is not geolocalized.")
            if contact_not_geolocalized:
                error_message = _(
                    "The address of the starting point is not geolocalized."
                )
            if same_address:
                error_message = _("Both addresses are the same.")
            if error_message:
                self.send_notification(error_message)
        else:
            if address_not_geolocalized:
                error_message = _("Some addresses are not geolocalized.")
                self.send_notification(error_message)
            if contact_not_geolocalized:
                error_message = _("Some starting points are not geolocalized.")
                self.send_notification(error_message)
            if same_address:
                error_message = _(
                    "Some addresses between contact and starting point are the same."
                )
                self.send_notification(error_message)

    def make_address_inline(self):
        """Make the address in one line from the different fields of the address.
        Used to geolocalize the address."""
        adresse = ""
        for elem in [
            self.street,
            self.street2,
            self.city,
            self.state_id.name,
            self.zip,
            self.country_id.name,
        ]:
            if elem:
                adresse = adresse + elem + ", "
        adresse = adresse[:-2]
        return adresse

    def geo_localize(self):
        """Override the geo_localize method to let us store
        the geolocalization of the address in the Odoo database."""
        for record in self:
            adresse = record.make_address_inline()

            geocode = self.env["geocode"]
            if geocode.is_already_geolocalized(adresse):
                _logger.debug("The address is already geolocalized")
                geocode = geocode.search([("x_tripestimator_address", "=", adresse)])[0]
                record.partner_latitude = geocode.x_tripestimator_latitude
                record.partner_longitude = geocode.x_tripestimator_longitude
            else:
                _logger.debug(
                    "The address is not geolocalized, calling the super method"
                )
                super(res_partner, record).geo_localize()
                geocode.create(
                    {
                        "x_tripestimator_latitude": record.partner_latitude,
                        "x_tripestimator_longitude": record.partner_longitude,
                        "x_tripestimator_address": adresse,
                    }
                )

    def create(self, values):
        """Override the create method to calculate the distance and the time
        between the contact and the starting point at the creation."""
        res = super(res_partner, self).create(values)
        res.calculate_distance()
        return res

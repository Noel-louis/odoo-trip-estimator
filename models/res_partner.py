# _ is used to translate the strings in the current language
from odoo import api, fields, models, _

import logging

_logger = logging.getLogger(__name__)


class res_partner(models.Model):
    _inherit = "res.partner"

    # starting point for the trip calculation
    address_contact_id = fields.Many2one(
        "res.partner",
        string=_("Address Contact"),
        default=lambda self: self.env.company.partner_id.id,
    )
    address_contact_ids = fields.One2many(
        "res.partner", "address_contact_id", string=_("Address Contact")
    )
    # calcul data
    distance = fields.Float(string=_("Distance float"))
    time = fields.Float(string=_("Time float"))

    # printed data
    distance_char = fields.Char(string=_("Distance"), compute="_compute_distance_char")
    time_char = fields.Char(string=_("Time"), compute="_compute_time_char")

    @api.depends("distance")
    def _compute_distance_char(self):
        # prettify the distance
        for record in self:
            if record.distance > 1000:
                record.distance_char = "{:.1f} km".format((record.distance / 1000))
            else:
                record.distance_char = str(record.distance) + " m"

    @api.depends("time")
    def _compute_time_char(self):
        # prettify the time
        for record in self:
            secondes = record.time % 60
            minutes = (record.time - secondes) / 60
            if minutes > 60:
                heures = (minutes - (minutes % 60)) / 60
                minutes = minutes % 60
                record.time_char = "{:.0f} h {:.0f} min".format(heures, minutes)
            else:
                record.time_char = "{:.0f} min".format(minutes)

    def calculate_distance(self):
        same_address = False
        address_not_geolocalized = False
        contact_not_geolocalized = False
        for record in self:
            record.geo_localize()
            record.address_contact_id.geo_localize()
            # calculate the distance and the time between the contact and the company
            if (
                record.partner_latitude == record.address_contact_id.partner_latitude
                and record.partner_longitude
                == record.address_contact_id.partner_longitude
            ):
                record.distance = 0
                record.time = 0
                same_address = True
            elif record.partner_latitude == 0 and record.partner_longitude == 0:
                address_not_geolocalized = True
            elif (
                record.address_contact_id.partner_latitude == 0
                and record.address_contact_id.partner_longitude == 0
            ):
                contact_not_geolocalized = True
            else:
                dist = record.env["distance"].compute_distance(
                    record.partner_latitude,
                    record.partner_longitude,
                    record.address_contact_id.partner_latitude,
                    record.address_contact_id.partner_longitude,
                )
                # set the values of the fields
                record.distance = dist.distance
                record.time = dist.travel_time

        if self.__len__() == 1:
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
                self.env["bus.bus"]._sendone(
                    self.env.user.partner_id,
                    "simple_notification",
                    {
                        "type": "warning",
                        "title": _("Warning"),
                        "message": error_message,
                    },
                )
        else:
            if address_not_geolocalized:
                error_message = _("Some addresses are not geolocalized.")
                self.env["bus.bus"]._sendone(
                    self.env.user.partner_id,
                    "simple_notification",
                    {
                        "type": "warning",
                        "title": _("Warning"),
                        "message": error_message,
                    },
                )
            if contact_not_geolocalized:
                error_message = _("Some starting points are not geolocalized.")
                self.env["bus.bus"]._sendone(
                    self.env.user.partner_id,
                    "simple_notification",
                    {
                        "type": "warning",
                        "title": _("Warning"),
                        "message": error_message,
                    },
                )
            if same_address:
                error_message = _(
                    "Some addresses between contact and starting point are the same."
                )
                self.env["bus.bus"]._sendone(
                    self.env.user.partner_id,
                    "simple_notification",
                    {
                        "type": "warning",
                        "title": _("Warning"),
                        "message": error_message,
                    },
                )

    @api.depends("address_contact_ids")
    def _compute_address_id(self):
        for record in self:
            if record.address_contact_ids:
                record.address_contact_id = record.address_contact_ids[0].id

    def _inverse_address_id(self):
        for record in self:
            if record.address_contact_id:
                record.address_contact_ids = [(4, record.address_contact_id.id)]

    def make_address_inline(self):
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
        for record in self:
            adresse = record.make_address_inline()

            geocode = self.env["geocode"]
            if geocode.is_already_geolocalized(adresse):
                _logger.debug("The address is already geolocalized")
                geocode = geocode.search([("address", "=", adresse)])[0]
                record.partner_latitude = geocode.latitude
                record.partner_longitude = geocode.longitude
            else:
                _logger.debug(
                    "The address is not geolocalized, calling the super method"
                )
                super(res_partner, record).geo_localize()
                geocode.create(
                    {
                        "latitude": record.partner_latitude,
                        "longitude": record.partner_longitude,
                        "address": adresse,
                    }
                )

    def create(self, values):
        res = super(res_partner, self).create(values)
        res.calculate_distance()
        return res

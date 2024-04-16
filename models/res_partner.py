# _ is used to translate the strings in the current language
from odoo import api, fields, models, _
from odoo.exceptions import UserError


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
        for record in self:
            # use the geolocation of the contact if it exists or calculate it using the module geolocate
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
                error_message = _("The addresses are the same. The distance is 0.")
                raise UserError(error_message)
            elif record.partner_latitude == 0 and record.partner_longitude == 0:
                error_message = _("The address is not geolocalized.")
                raise UserError(error_message)

            elif (
                record.address_contact_id.partner_latitude == 0
                and record.address_contact_id.partner_longitude == 0
            ):
                error_message = _(
                    "The address of the contact is not geolocalized. Please change its address."
                )
                raise UserError(error_message)
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

    @api.depends("address_contact_ids")
    def _compute_address_id(self):
        for record in self:
            if record.address_contact_ids:
                record.address_contact_id = record.address_contact_ids[0].id

    def _inverse_address_id(self):
        for record in self:
            if record.address_contact_id:
                record.address_contact_ids = [(4, record.address_contact_id.id)]

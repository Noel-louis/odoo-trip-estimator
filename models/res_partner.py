from odoo import api, fields, models
from . import geocode


class res_partner(models.Model):
    _inherit = "res.partner"

    # calcul data
    latitude = fields.Float(string="Latitude")
    longitude = fields.Float(string="Longitude")
    distance = fields.Float(string="Distance float")
    time = fields.Float(string="time float")

    # printed data
    distance_char = fields.Char(string="Distance", compute="_compute_distance_char")
    time_char = fields.Char(string="time", compute="_compute_time_char")

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
            # create an address for the contact without the name for geolocation
            adresse = ""
            for elem in [
                record.street,
                record.street2,
                record.city,
                record.state_id.name,
                record.zip,
                record.country_id.name,
            ]:
                if elem:
                    adresse = adresse + elem + ", "
            adresse = adresse[:-2]
            geo = self.env["geocode"].geocode_address(adresse)
            record.latitude = geo.latitude
            record.longitude = geo.longitude

            # create an address for the company without the name for geolocation
            company = self.env.company
            adresse_company = ""
            for elem in [
                company.partner_id.street,
                company.partner_id.street2,
                company.partner_id.city,
                company.partner_id.state_id.name,
                company.partner_id.zip,
                company.partner_id.country_id.name,
            ]:
                if elem:
                    adresse_company = adresse_company + elem + ", "
            adresse_company = adresse_company[:-2]

            # calculate the geolocation of the company
            geo_company = self.env["geocode"].geocode_address(adresse_company)
            # calculate the distance and the time between the contact and the company
            dist = self.env["distance"].compute_distance(
                record.latitude,
                record.longitude,
                geo_company.latitude,
                geo_company.longitude,
            )
            # set the values of the fields
            record.distance = dist.distance
            record.time = dist.travel_time

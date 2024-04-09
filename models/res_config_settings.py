from odoo import api, models, fields
import openrouteservice as ors


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    key = fields.Char(
        string="OpenRouteService API Key", config_parameter="odoo-trip-estimator.key"
    )

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res.update(
            {
                "key": self.env["ir.config_parameter"]
                .sudo()
                .get_param("odoo-trip-estimator.key")
            }
        )
        return res

# Copyright 2024 Therp BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    forecast_line_priority_1_date = fields.Date(
        inverse="_inverse__compute_forecast_line_priority_1_date_str"
    )
    forecast_line_priority_1_date_str = fields.Char(
        config_parameter="project_forecast_line_priority.priority_1"
    )
    forecast_line_priority_2 = fields.Integer(
        config_parameter="project_forecast_line_priority.priority_2"
    )
    forecast_line_priority_3 = fields.Integer(
        config_parameter="project_forecast_line_priority.priority_3"
    )

    def _inverse__compute_forecast_line_priority_1_date_str(self):
        """As config_parameters does not accept Date field,
        we store the date formated string into a Char config field"""
        for setting in self:
            if setting.forecast_line_priority_1_date:
                setting.forecast_line_priority_1_date_str = fields.Date.to_string(
                    setting.forecast_line_priority_1_date
                )

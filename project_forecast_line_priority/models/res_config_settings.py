# Copyright 2024 Therp BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models

TYPE_FORECAST_ENDDATE = [
    ("none", "None"),
    ("date", "Date"),
    ("delta", "Delta (in days)"),
]


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    forecast_line_priority_1_date = fields.Date(
        inverse="_inverse_forecast_line_priority_1_date_str"
    )
    forecast_line_priority_1_date_str = fields.Char(
        config_parameter="project_forecast_line_priority.priority_1_date"
    )
    forecast_line_priority_2_date = fields.Date(
        inverse="_inverse_forecast_line_priority_1_date_str"
    )
    forecast_line_priority_2_date_str = fields.Char(
        config_parameter="project_forecast_line_priority.priority_2_date"
    )
    forecast_line_priority_3_date = fields.Date(
        inverse="_inverse_forecast_line_priority_1_date_str"
    )
    forecast_line_priority_3_date_str = fields.Char(
        config_parameter="project_forecast_line_priority.priority_3_date"
    )
    forecast_line_priority_1 = fields.Integer(
        config_parameter="project_forecast_line_priority.priority_1_delta"
    )
    forecast_line_priority_2 = fields.Integer(
        config_parameter="project_forecast_line_priority.priority_2_delta"
    )
    forecast_line_priority_3 = fields.Integer(
        config_parameter="project_forecast_line_priority.priority_3_delta"
    )
    forecast_line_priority_1_selection = fields.Selection(
        TYPE_FORECAST_ENDDATE,
        default="none",
        config_parameter="project_forecast_line_priority.priority_1_selection",
        required=True,
    )
    forecast_line_priority_2_selection = fields.Selection(
        TYPE_FORECAST_ENDDATE,
        default="none",
        config_parameter="project_forecast_line_priority.priority_2_selection",
        required=True,
    )
    forecast_line_priority_3_selection = fields.Selection(
        TYPE_FORECAST_ENDDATE,
        default="none",
        config_parameter="project_forecast_line_priority.priority_3_selection",
        required=True,
    )

    def _inverse_forecast_line_priority_1_date_str(self):
        """As config_parameters does not accept Date field,
        we store the date formated string into a Char config field"""
        for setting in self:
            if setting.forecast_line_priority_1_date:
                setting.forecast_line_priority_1_date_str = fields.Date.to_string(
                    setting.forecast_line_priority_1_date
                )
            if setting.forecast_line_priority_2_date:
                setting.forecast_line_priority_2_date_str = fields.Date.to_string(
                    setting.forecast_line_priority_2_date
                )
            if setting.forecast_line_priority_3_date:
                setting.forecast_line_priority_3_date_str = fields.Date.to_string(
                    setting.forecast_line_priority_3_date
                )

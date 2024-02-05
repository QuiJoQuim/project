# Copyright 2024 Therp BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from datetime import timedelta

from odoo import fields, models


class ProjectTask(models.Model):
    _inherit = "project.task"

    def write(self, vals):
        """Set forecast_date_planned_end based on priority"""
        # If user sets end date manually
        if "forecast_date_planned_end" in vals or "date_deadline" in vals:
            return super().write(vals)
        if "priority" not in vals:
            return super().write(vals)
        priority = vals.get("priority", -5)
        for this in self:
            # date deadline is set, so ignore this one
            if this.date_deadline:
                continue
            # if priority is not set, do nothing
            if int(priority) < 0:
                continue
            forecast_date_planned_end = self._get_forecast_date_planned(
                priority=priority
            )
            if forecast_date_planned_end:
                vals["forecast_date_planned_end"] = forecast_date_planned_end
        return super().write(vals)

    def _get_forecast_date_planned(self, priority=None):
        config_model = self.env["ir.config_parameter"]
        priority = priority or self.priority
        selection = config_model.get_param(
            "project_forecast_line_priority.priority_%s_selection" % priority
        )
        if selection == "none":
            return False
        if selection == "delta":
            return fields.Date.today() + timedelta(
                days=int(
                    config_model.get_param(
                        "project_forecast_line_priority.priority_%s_delta" % priority
                    )
                )
            )
        if selection == "date":
            return config_model.get_param(
                "project_forecast_line_priority.priority_%s_date" % priority
            )

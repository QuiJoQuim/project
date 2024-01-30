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
        config_model = self.env["ir.config_parameter"]
        priority = int(vals.get("priority", 0))
        today = fields.Date.today()
        for this in self:
            # date deadline is set, so ignore this one
            if this.date_deadline:
                continue
            # if priority is 0, do nothing
            if priority < 1:
                continue
            if priority == 1:
                # add weeks to end date
                vals["forecast_date_planned_end"] = config_model.get_param(
                    "project_forecast_line_priority.priority_1"
                )
            else:
                # priorities 2 and 3
                # add days to end date
                interval = timedelta(
                    days=int(
                        config_model.get_param(
                            "project_forecast_line_priority.priority_%s" % priority
                        )
                    )
                )
                vals["forecast_date_planned_end"] = today + interval
        return super().write(vals)

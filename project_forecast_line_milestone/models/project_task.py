# Copyright 2024 Therp BV <https://therp.nl>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, models


class ProjectTask(models.Model):
    _inherit = "project.task"

    def _forecast_date_planned_end_depends_list(self):
        """Returns a list of fields to trigger recomputation"""
        return super()._forecast_date_planned_end_depends_list() + [
            "milestone_id",
            "milestone_id.deadline",
        ]

    @api.depends(_forecast_date_planned_end_depends_list)
    def _compute_forecast_date_planned_end(self):
        """Override method to use milestone_id.deadline"""
        res = super()._compute_forecast_date_planned_end()
        for this in self:
            if not this.milestone_id.deadline:
                continue
            this.forecast_date_planned_end = this.milestone_id.deadline
        return res

    def _get_forecast_date_planned(self, priority=None):
        """Do not set forecast end if there exists a milestone date"""
        self.ensure_one()
        if self.milestone_id.deadline:
            return False
        return super()._get_forecast_date_planned(priority=priority)

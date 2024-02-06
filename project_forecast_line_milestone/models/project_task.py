# Copyright 2024 Therp BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, models


class ProjectTask(models.Model):
    _inherit = "project.task"

    @api.depends("date_deadline", "milestone_id", "milestone_id.target_date")
    def _compute_forecast_date_planned_end(self):
        """Override method to use milestone_id.target_date"""
        for this in self:
            if this.milestone_id.target_date:
                this.forecast_date_planned_end = this.milestone_id.target_date
                continue
            if this.date_deadline:
                this.forecast_date_planned_end = this.date_deadline
                continue
            this.forecast_date_planned_end = this.forecast_date_planned_end

    def _get_forecast_date_planned(self, priority=None):
        """Do not set forecast end if there exists a milestone date"""
        self.ensure_one()
        if self.milestone_id.target_date:
            return False
        return super()._get_forecast_date_planned(priority=priority)

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for record in records:
            if not record.milestone_id.target_date:
                continue
            record.forecast_date_planned_end = record.milestone_id.target_date
        return records

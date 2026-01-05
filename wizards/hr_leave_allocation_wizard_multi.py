# -*- coding: utf-8 -*-
from odoo import api, fields, models,_


class HrLeaveAllocationWizardMulti(models.TransientModel):
    _inherit = 'hr.leave.allocation.generate.multi.wizard'
    def action_generate_allocations(self):
        self.ensure_one()
        employees = self._get_employees_from_allocation_mode()
        vals_list = self._prepare_allocation_values(employees)
        if vals_list:
            allocations = self.env['hr.leave.allocation'].with_context(
                mail_notify_force_send=False,
                mail_activity_automation_skip=True
            ).create(vals_list)
            for alloc in allocations:
                if alloc.allocation_type == 'accrual' and alloc.accrual_plan_id:
                    alloc._onchange_date_from()
            allocations.filtered(lambda c: c.validation_type != 'no_validation').action_validate()
            return {
                'type': 'ir.actions.act_window',
                'name': _('Generated Allocations'),
                "views": [[self.env.ref('hr_holidays.hr_leave_allocation_view_tree').id, "list"], [self.env.ref('hr_holidays.hr_leave_allocation_view_form_manager').id, "form"]],
                'view_mode': 'list',
                'res_model': 'hr.leave.allocation',
                'domain': [('id', 'in', allocations.ids)]
            }


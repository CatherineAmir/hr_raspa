from odoo import fields, models, api


class HrLeaveType(models.Model):
    _inherit='hr.leave.type'

    used_in_end_payslip=fields.Boolean(string="Used In End Payslip",default=False)

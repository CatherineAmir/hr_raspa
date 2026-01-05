from odoo import fields, models, api
from datetime import date


class BankPayroll(models.TransientModel):
    _name = 'bank_payroll.wizard'
    _description = 'Bank Payroll wizard'

    file_date = fields.Date(required=True, default=lambda self: date.today(), string="File Date")
    value_date = fields.Date(required=True, default=lambda self: date.today(), string="Value Date")
    narrative = fields.Selection(selection=[
        ("Salary_Fixed_Allowance", "Salary and Fixed Allowance"),
        ("Variable_Allowance", "Variable Allowance"),
        ("Bonus", "Bonus"),
        ("EUR_commissions", "EUR Commissions"), ("STERLING_commissions", "STERLING Commissions"),
        ("Profit Share", "Profit Share"),
        ("exceptional_bonus", "Exceptional Bonus"),
    ], default="Salary_Fixed_Allowance",
        string="Narrative", required=True)
    creditor_bic_code = fields.Char(string="Creditor BIC Code", default="CIBEEGCXXXX")
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.user.company_id.currency_id,
                                  string="Currency")

    company_account_number = fields.Char(default="100008830821", string="Company Account Number")
    company_account_name = fields.Char(default="MASTERS TRAVEL SERVICE", string="Company Account Name")
    batch_ids = fields.Many2many('hr.payslip.run', string="Batches")
    payslips_ids = fields.Many2many('hr.payslip', string="Payslips", required=True)
    report_type = fields.Selection([("CIB Bank", "CIB Bank")
                                       , ("All Payroll and JV", "All Payroll and JV"),
                                    ("SAP JV","SAP JV"),("Master Payslip","Master Payslip"),],
                                   default="CIB Bank")

    @api.onchange('batch_ids')
    def _compute_payslips_ids(self):
        for r in self:
            if r.batch_ids:
                slips_ids = r.batch_ids.mapped("slip_ids").ids
                r.payslips_ids = slips_ids
            else:
                return

    def generate_payslip_report(self):

        docs = {
            'form': self.read()[0],
            'required_model': 'hr.payslip',
            'slip_ids': self.payslips_ids,
            'model': self._name,

        }

        return self.env.ref('hr_raspa.bank_payroll_all_excel').report_action(self, data=docs)

    def generate_insurance_report(self):

        docs = {
            'form': self.read()[0],
            'required_model': 'hr.payslip',
            'slip_ids': self.payslips_ids,
            'model': self._name,

        }

        return self.env.ref('hr_raspa.insurance_report_payroll_all_excel').report_action(self, data=docs)

    def generate_payslip_breakdown_report(self):

        docs = {
            'form': self.read()[0],
            'required_model': 'hr.payslip',
            'slip_ids': self.payslips_ids,
            'model': self._name,

        }

        return self.env.ref('hr_raspa.payslip_break_down_report_excel').report_action(self, data=docs)

    # @api.constrains('narrative', 'batch_ids')
    # def check_access_GM(self):
    #     for rec in self:
    #         gm_group = self.env.ref('hr_egypt.group_general_manager')
    #         user_has_gm = gm_group in self.env.user.groups_id
    #         if not user_has_gm and self.report_type!="Master Payslip":
    #             for batch in rec.batch_ids:
    #                 if rec.narrative == 'Variable_Allowance' and not batch.check_variable_allowance:
    #                     raise models.ValidationError(
    #                         f"Batch {batch.name} not approved Variable Allowance by General Manager")
    #                 elif rec.narrative == 'Salary_Fixed_Allowance' and not batch.check_salary_fixed_allowance:
    #                     raise models.ValidationError(
    #                         f"Batch {batch.name} not approved Salary Fixed Allowance by General Manager")
    #                 elif rec.narrative == 'Bonus' and not batch.check_bonus:
    #                     raise models.ValidationError(f"Batch {batch.name} not approved Bonus by General Manager")
    #                 elif rec.narrative == 'EUR_commissions' and not batch.check_eur_commissions:
    #                     raise models.ValidationError(
    #                         f"Batch {batch.name} not approved EUR Commissions by General Manager")
    #                 elif rec.narrative == 'STERLING_commissions' and not batch.check_sterling_commissions:
    #                     raise models.ValidationError(
    #                         f"Batch {batch.name} not approved STERLING Commissions by General Manager")
    #                 elif rec.narrative == 'Profit Share' and not batch.check_profit_share:
    #                     raise models.ValidationError(f"Batch {batch.name} not approved Profit Share by General Manager")

from odoo import fields, models, api


class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    def add_secondary_currency_data(self):
        for slip in self:
            lines = slip.input_line_ids.filtered(lambda line: line.secondary_currency)
            rules = slip.line_ids
            for line in lines:
                rule_ids = rules.filtered(lambda rule: line.code in rule.salary_rule_id.condition_python)
                if rule_ids:
                    for rule_id in rule_ids:
                        rule_id.secondary_currency = True
                        rule_id.secondary_currency_id = line.secondary_currency_id
                        rule_id.secondary_amount = rule_id.total / line.exchange_rate
                        rule_id.exchange_rate = line.exchange_rate



    def compute_sheet(self):
        super(HrPayslip, self).compute_sheet()
        self.add_secondary_currency_data()
        return True
class PayslipLine(models.Model):
    _inherit = "hr.payslip.line"

    secondary_currency=fields.Boolean(string="Secondary Currency",default=False)
    secondary_currency_id=fields.Many2one('res.currency', string="Secondary Currency")
    secondary_amount=fields.Monetary(string="Secondary Amount", currency_field='secondary_currency_id')
    exchange_rate=fields.Float(string="Exchange Rate", default=1.0)
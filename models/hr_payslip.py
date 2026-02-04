from odoo import fields, models, api


class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    secondary_currency_id=fields.Many2one("res.currency", string="Currency",related="struct_id.currency_id",store=True)
    currency_rate=fields.Float(string="Currency Rate",default=1.0,readonly=True)

    def add_secondary_currency_data(self):
        for slip in self:
           for line in slip.line_ids:
               line.secondary_amount = line.total / slip.currency_rate
            # rules = slip.line_ids
            # for line in lines:
            # rule_ids = line.filtered(lambda rule: rule.code in rule.salary_rule_id.condition_python)
            #     if rule_ids:
            # for rule_id in rules:
            #     rule_id.secondary_currency = True
            #     rule_id.secondary_currency_id = line.secondary_currency_id
            #     rule_id.secondary_amount = rule_id.total / line.exchange_rate
            #     rule_id.exchange_rate = line.exchange_rate




    def compute_sheet(self):
        super(HrPayslip, self).compute_sheet()
        self.add_secondary_currency_data()
        return True
class PayslipLine(models.Model):
    _inherit = "hr.payslip.line"

    secondary_currency=fields.Boolean(string="Secondary Currency",compute="_compute_is_secondary_currency",store=True)
    secondary_currency_id=fields.Many2one('res.currency', string="Secondary Currency",related="slip_id.secondary_currency_id",store=True)
    secondary_amount=fields.Monetary(string="Secondary Amount", currency_field='secondary_currency_id')
    exchange_rate=fields.Float(string="Exchange Rate", related="slip_id.currency_rate",store=True)


    @api.depends("slip_id.secondary_currency_id","slip_id.currency_id")
    def _compute_is_secondary_currency(self):
        for r in self:
            if r.slip_id.secondary_currency_id!=r.slip_id.currency_id:
                r.secondary_currency = True
            else:
                r.secondary_currency = False

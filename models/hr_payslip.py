from odoo import fields, models, api


class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    secondary_currency_id=fields.Many2one("res.currency", string="Currency",related="struct_id.currency_id",store=True)
    currency_rate=fields.Float(string="Currency Rate",default=1.0,readonly=True)


    def employee_resign(self):
        self.ensure_one()
        employee_id=self.employee_id.id
        end_date = self.contract_id.date_end or self.date_to
        # todo for Accural plan
        # today=date.today()
        time_off_types=self.env['hr.leave.type'].search([("used_in_end_payslip",'=',True)])
        allocation_days=self.env['hr.leave.allocation'].search([("employee_id",'=',employee_id),("holiday_status_id","in",time_off_types.ids),'|',("date_to",'=',False),("date_to",'>=',end_date)])
        print("allocation_days",allocation_days)
        # if len(allocation_days)>1:
        #     raise ValidationError(_("There are more than one allocation for time off active %s",','.join(allocation_days.mapped("name"))))
        if len(allocation_days)==0:
            number_of_days_display=0
        else:

            # allocation_days=allocation_days[0]
            number_of_days_display=sum(allocation_days.mapped("number_of_days_display"))
        taken_leaves=self.env['hr.leave'].search([("employee_id",'=',employee_id),("holiday_status_id","in",time_off_types.ids),('state','=','validate')])
        taken_days=sum(taken_leaves.mapped("number_of_days"))
        # print("taken_days",taken_days)
        #
        # print("number_of_days_allocation",number_of_days_display)
        # print("taken_days",taken_days)

        # allocation date
        allocation_start_date=allocation_days[0].date_from
        allocation_end_date=allocation_days[0].date_to
        # print("allocation_start_date",allocation_start_date)
        # print("allocation_end_date",allocation_end_date)
        if allocation_start_date<allocation_end_date:
            allocation_period=(allocation_end_date-allocation_start_date).days/30
            # print("allocation_period",allocation_period)


            worked_months=(end_date - allocation_start_date).days/30
            # print("worked_months",worked_months)

            month_allocation=number_of_days_display/allocation_period

            # print("total_months_allocation",month_allocation)

            theoretical_days_taken=month_allocation*worked_months
            # print("theoretical_days_taken",theoretical_days_taken)
        else:
            theoretical_days_taken=0

        difference=round(theoretical_days_taken-taken_days,0)
        # print("difference",difference)
                # if difference>0:
        input="timeoff_settlement"
        InputType=self.env['hr.payslip.input.type']
        input_id=InputType.search([('code','=',input)])
        if not input_id:
            input_id=InputType.create({
                "name":"Timeoff Settlement",
                "code":input,
                "struct_ids":[self.struct_id.id],
            })

        self.env['hr.payslip.input'].create({
            'input_type_id':input_id.id,
            'amount':difference,
            "name":"Timeoff Settlement",
            'payslip_id':self.id,
        })

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

from odoo import fields, models, api


class PayrollStructure(models.Model):
    _inherit= 'hr.payroll.structure'

    def _get_default_currency(self):
        return self.env.company.currency_id.id

    currency_id = fields.Many2one("res.currency", string="Currency",default=_get_default_currency)

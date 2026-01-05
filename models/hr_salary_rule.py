from odoo import fields, models, api


class HrRule(models.Model):
    """ This model represents hr.rule."""
    _inherit='hr.salary.rule'
    secondary_currency = fields.Boolean(string="Secondary Currency", default=False)



from odoo import fields, models, api


class HrContract(models.Model):
    _inherit="hr.contract"

    secondary_currency_id=fields.Many2one("res.currency",related="structure_type_id.default_struct_id.currency_id",store=True)
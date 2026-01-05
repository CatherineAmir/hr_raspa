from odoo import fields, models, api
from datetime import datetime

class PayslipMasterReportExcel(models.AbstractModel):
    _name="report.hr_raspa_payslip_breakdown_report"
    _inherit = 'report.report_xlsx.abstract'
    _description = "Payslip Master Report"

    def generate_xlsx_report(self, workbook, data, lines):




        cell_format = workbook.add_format({'align': 'center',
                                           'valign': 'vcenter',
                                           'border': 1,
                                           'bold': True,
                                           'bg_color': '#FFFFFF', 'text_wrap': True,
                                           'num_format': '#,##0.00'})

        header_format = workbook.add_format({'align': 'center',
                                             'valign': 'vcenter',
                                             'border': 2,
                                             'bold': True,
                                             'bg_color': '#92d050'})
        yellow_format = workbook.add_format(
            {'align': 'center', 'bold': True, 'bg_color': "#ffc000", 'border': 2, 'num_format': '#,##0.00'})

        date_format_yellow = workbook.add_format({
            # "num_format":'@',
            'align': 'center',
            'valign': 'vcenter',
            'border': 2,
            'bold': True,
            'bg_color': '#ffc000',
        })
        sheet = workbook.add_worksheet("Masters Payslip All")

        payslips_ids = self.env["hr.payslip"].search([("id", "in", data["form"]["payslips_ids"])])
        struct_ids=payslips_ids.mapped("struct_id")
        if len(struct_ids) > 1:
            raise UserWarning("You can't generate report for multiple salary structures, please select one salary structure.")
        else:
            headers = ["Employee Code", "Employee Name", "Employee Arabic","Joining Date", "Department", "Job Position"]
            # rules=struct_ids[0].mapped("rule_ids").mapped("name")


            for i in range(0, len(headers)):

                sheet.write_string(0, i, str(headers[i]), header_format)
            col=len(headers)
            rules=struct_ids[0].rule_ids
            extra_rules = rules.filtered(lambda x:x.secondary_currency)
            sheet.set_column(0, len(headers) + len(rules)+len(extra_rules), width=40)


            for i in range(0, len(rules)):
                if rules[i].secondary_currency:
                    sheet.write_string(0, col+i, str(rules[i].name + " EGP"), header_format)
                    col = col + 1
                    sheet.write_string(0, col+i, str(rules[i].name + " Currency" ), header_format)

                else:
                    sheet.write_string(0, col+i, str(rules[i].name ), header_format)


            row = 1
            totals= [0.0] * (len(struct_ids[0].rule_ids)+len(struct_ids[0].rule_ids.filtered(lambda x:x.secondary_currency)))
            # print("totals", totals)
            # print("len(totals)", len(totals))

            for i in range(0, len(payslips_ids)):

                payslip = payslips_ids[i]
                employee = payslip.employee_id
                currency = payslip.currency_id.symbol if payslip.currency_id else ""
                sheet.write_string(row, 0, str(employee.employee_code), cell_format)
                sheet.write_string(row, 1, str(employee.name), cell_format)
                sheet.write_string(row, 2, str(employee.employee_name_arabic), cell_format)
                sheet.write_string(row, 3, str(employee.first_contract_date or ""), cell_format)
                sheet.write_string(row, 4, str(employee.department_id.name or ""), cell_format)
                sheet.write_string(row, 5, str(employee.job_id.name or ""), cell_format)
                col=6
                for j in range(0, len(struct_ids[0].rule_ids)):
                    rule = struct_ids[0].rule_ids[j]
                    payslip_line=payslip.line_ids.filtered(lambda x: x.salary_rule_id.id == rule.id)
                    value = payslip_line.total

                    sheet.write_number(row,col, abs(value), cell_format)
                    secondary_amount = payslip_line.secondary_amount
                    totals[col-6] += abs(value) if value else 0.0
                    if payslip_line.secondary_currency:
                        col += 1

                        sheet.write_number(row, col ,abs(secondary_amount), cell_format)
                        totals[col-6] += abs(secondary_amount) if secondary_amount else 0.0
                    col += 1
                row += 1
            for j in range(0, len(totals)):
                if totals[j] > 0:
                    sheet.write_number(row, j + 6, totals[j], yellow_format)
                else:
                    sheet.write_number(row, j + 6, totals[j], yellow_format)



from odoo import fields, models, api
from datetime import datetime

class PayslipMasterReportExcel(models.AbstractModel):
    _name="report.hr_raspa.payslip_breakdown_report"
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
            headers = ["Employee Name","Joining Date", "Department", "Job Position"]+struct_ids[0].mapped("rule_ids").mapped("name")

            sheet.set_column(0, len(headers), width=40)
            for i in range(0, len(headers)):

                sheet.write_string(0, i, str(headers[i]), header_format)
            row = 1
            totals= [0.0] * (len(struct_ids[0].rule_ids))
            for i in range(0, len(payslips_ids)):

                payslip = payslips_ids[i]
                employee = payslip.employee_id
                currency = payslip.currency_id.symbol if payslip.currency_id else ""
                # sheet.write_string(row, 0, str(employee.employee_code), cell_format)
                sheet.write_string(row, 0, str(employee.name), cell_format)
                # sheet.write_string(row, 2, str(employee.employee_name_arabic or ""), cell_format)
                sheet.write_string(row, 1, str(employee.first_contract_date or ""), cell_format)
                sheet.write_string(row, 2, str(employee.department_id.name or ""), cell_format)
                sheet.write_string(row, 3, str(employee.job_id.name or ""), cell_format)


                for j in range(0, len(struct_ids[0].rule_ids)):
                    rule = struct_ids[0].rule_ids[j]
                    value = payslip.line_ids.filtered(lambda x: x.salary_rule_id.id == rule.id).total

                    sheet.write_number(row, j + 4, abs(value), cell_format)

                    totals[j] += abs(value) if value else 0.0
                row += 1
            for j in range(0, len(totals)):
                if totals[j] > 0:
                    sheet.write_number(row, j + 4, totals[j], yellow_format)
                else:
                    sheet.write_number(row, j + 4, totals[j], yellow_format)
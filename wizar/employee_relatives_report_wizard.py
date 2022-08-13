from odoo import models, fields, api,_
 
class EmployeeRelativesReportWizard(models.TransientModel):

    _name = 'employee.relatives.report.wizard'
    _description = 'create report from wizard'

    employee_id=fields.Many2one('employee.relatives',string='employee')


    def employee_relatives_report_action(self):
        employee_relatives=self.env['relatives'].search_read([('employee_id','=',self.employee_id.id)])
        data={
            'form':self.read()[0],
            'employee_relatives':employee_relatives,
        }
        print(employee_relatives)
        return self.env.ref('employee_relatives.employee_relatives_report_action').report_action(self,data=data)

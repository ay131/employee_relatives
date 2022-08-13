# -*- coding: utf-8 -*-
from datetime import date, datetime

import dateutil.utils
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError
from odoo import models, fields, api ,_

# =====================[const value]============================
state = [
    ('draft', 'Draft'),
    ('confirmed', 'Confirmed'),
    ('ended', 'Ended'),
    ('canceled', 'Canceled'),
]
# ============================================================
# =========================[ Estate Property model ]===================
class EmployeeRelatives(models.Model):
    # =========================[ model defination ]===================
    _name = 'employee.relatives'
    _description = 'employee relatives'
    _rec_name='employee_id'
    # =================================================================
    # =========================[SQL costrains=====employee_id=]===================
    _sql_constraints = [
        ('employee_id_uniq', 'unique(employee_id)', 'The employee already existe .')
    ]
    # =================================================================
    # =========================[main field]===================
    code_name=fields.Char(string='code',copy=False, readonly=True, default=lambda x: _('New'))
    state = fields.Selection(selection=state,string='status',tracking=True, default=state[0][0])
    # =================================================================
    # =========================[relashional fields ]===================
    employee_id = fields.Many2one('hr.employee',string='Employee',ondelete='cascade',domain="[('contract_ids.state', '=','open')]")
    relative_ids = fields.One2many('relatives','employee_id',ondelete='cascade',string='relatives')
    last_change_state = fields.Char(string='status change by',readonly=True,copy=False)
    user_id=fields.Integer(string='user id',readonly=True,copy=False,default=lambda self:self.env.user.id)

    # ================================================================
    # =========================[related fields ]===================
    employee_phone=fields.Char(related='employee_id.work_phone',readonly=True,string='Phone')
    # =================================================================
    # =========================[computed fields ]===================
    relatives_count = fields.Integer(compute='_compute_relatives_count',store=True,string='relatives count',default=0)
    # =================================================================

    # =========================[computed functions ]===================
    # =======[_compute_relatives_count]==========
    @api.depends('relative_ids')
    def _compute_relatives_count(self):
        self.relatives_count=self.env['relatives'].search_count([('employee_id','=',self.employee_id.name)])
        return self.relatives_count
    # ================================================================
    # ================[create overrid]===================================
    @api.model
    def create(self, vals):
        if vals.get('code_name', _('New')) == _('New'):
            vals['code_name'] = self.env['ir.sequence'].next_by_code('employee.relatives.sequence') or _('New')
        res = super(EmployeeRelatives, self).create(vals)
        return res
    # ==============================[onchange functions ]===================
    # ========[_onchange_status ]========
    @api.onchange("state")
    def _onchange_state(self):
         self.last_change_state = self.env.user.name

    # ========[_onchange_employee_id CHK contract ]========
    @api.onchange("employee_id")
    def _onchange_employee_id(self):
        d=date.today()
        for rec in self.employee_id.contract_ids:
            res=rec.date_end
            if  res !=False:
                if res<=d :
                    self.state=state[2][0]
            else:
                self.state=state[1][0]
    # ================================================================
    # =========================[action functions]===================
    # ========[action_do_cancal ]========
    def action_do_cancal(self):
        self.state = state[3][0]
    # ========[action_do_draft ]========
    def action_do_draft(self):
                self.state = state[0][0]
    # ================================================================

    # =========================[corn job  functions]===================
    # ========[state_corn_job ]========
    def state_corn_job(self):
        for rec in self.employee_id.contract_ids:
            if rec.date_end !=False:
                contract_delta =relativedelta(datetime.now(),rec.date_end)
                if contract_delta.years==0 and contract_delta.months==0 and contract_delta.age.days==0:
                    self.state = state[2][0]
    # ================================================================

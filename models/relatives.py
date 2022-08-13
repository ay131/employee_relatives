# -*- coding: utf-8 -*-
from datetime import date, datetime

from dateutil.relativedelta import relativedelta
from odoo import models, fields, api
# ===================[const value]==============================
relationship_dgree = [
    ('father','Father'),
    ('mother','Mother'),
    ('husband','Husband'),
    ('wife','Wife'),
    ('son','Son'),
    ('daughter','Daughter')
]

# =================================================
# =========================[ Relatives model ]===================
class Relatives(models.Model):
    # =========================[ model defination ]===================
    _name = 'relatives'
    _description = 'employee relatives and relationship'
    # =================================================================

    # =========================[main field]===================
    name = fields.Char(string='name',required=True)
    date_of_birth = fields.Date(string='birth date', required=True)
    relation_degree = fields.Selection(selection=relationship_dgree, string='relation degree',required=True)
    # =================================================================

    # =========================[relation fields]===================
    employee_id = fields.Many2one('employee.relatives', string="relative's employee",readonly=True)
    user_id=fields.Integer(string='user id',readonly=True,copy=False,default=lambda self:self.env.user.id)
    # ================================================================

    # =========================[compute fields]===================
    age = fields.Integer(compute='_compute_age', string="age", store=True, readonly=True)
    # ================================================================

    # =========================[computed functions ]===================
    # _compute_age founction
    @api.depends('date_of_birth')
    def _compute_age(self):
        for record in self:
            age = relativedelta(datetime.now(), record.date_of_birth)
            record.age = age.years + (age.months / 12)
    # ====================================================================

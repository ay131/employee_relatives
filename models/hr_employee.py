# -*- coding: utf-8 -*-

from odoo import models, fields, api

# =========================[  Hr Employee model ]===================
class HrEmployee(models.Model):
    # =========================[ model defination ]===================
    _inherit='hr.employee'
    # =================================================================

    # =========================[relashional fields ]===================
    relative_ids = fields.One2many('employee.relatives','employee_id',string='Relatives')
    # ================================================================

# -*- coding: utf-8 -*-
from datetime import timedelta
from openerp import models, fields, api, exceptions, _


class Learning(models.Model):
    _name = 'academy.learning'
    _inherit = 'mail.thread'
    _parent_name = "parent_id"
    _parent_store = True
    _parent_order = 'sequence, name'
    _order = "sequence"
    
    name = fields.Char(string="Name", required=True)
    sequence = fields.Integer("Sequence", select=True)
    parent_id = fields.Many2one('academy.learning','Parent Skill', select=True, ondelete='cascade')
    child_ids = fields.One2many('academy.learning', 'parent_id', string='Child Skills')
    parent_left = fields.Integer('Left Parent', select=1)
    parent_right = fields.Integer('Right Parent', select=1)
        
    _sql_constraints = [
        ('name_unique',
         'UNIQUE(name)',
         "The learning name must be unique"),
    ]

# -*- coding: utf-8 -*-
from datetime import timedelta
from openerp import models, fields, api, exceptions, _


class ProfLearn(models.Model):
    _name = 'academy.proflearn'
    
    professor_id = fields.Many2one('academy.professor')
    learn_id = fields.Many2one('academy.learning')
    skill = fields.Selection([('0', 'Poor'), ('1', 'Standard'), ('2', 'Good'), ('3', 'Awesome')], "Skill")
    

class Professor(models.Model):
    _name = 'academy.professor'
    _inherit = 'mail.thread'
    
    name = fields.Char(string="Name", required=True)
    picture = fields.Binary()
    learn_ids = fields.Many2many('academy.learning', 
                                relation='academy_proflearn', 
                                column1='professor_id', 
                                column2='learn_id')
    proflearn_ids = fields.One2many('academy.proflearn', 'professor_id')
    
    _sql_constraints = [
        ('name_unique',
         'UNIQUE(name)',
         "The professor name must be unique"),
    ]
    
class Learning(models.Model):
    _name = 'academy.learning'
    _inherit = 'mail.thread'
    _parent_name = "parent_id"
    _parent_store = True
    _parent_order = 'sequence, name'
    _order = "sequence"
    
    name = fields.Char(string="Name", required=True)
    picture = fields.Binary()
    sequence = fields.Integer("Sequence", select=True)
    parent_id = fields.Many2one('academy.learning','Parent Skill', select=True, ondelete='cascade')
    child_ids = fields.One2many('academy.learning', 'parent_id', string='Child Skills')
    parent_left = fields.Integer('Left Parent', select=1)
    parent_right = fields.Integer('Right Parent', select=1)
    professor_ids = fields.Many2many('academy.professor', 
                                relation='academy_proflearn', 
                                column1='learn_id', 
                                column2='professor_id')
    proflearn_ids = fields.One2many('academy.proflearn', 'learn_id')
    
    _sql_constraints = [
        ('name_unique',
         'UNIQUE(name)',
         "The learning name must be unique"),
    ]

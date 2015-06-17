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
    nbr_skills = fields.Integer('N° of skills', compute='_get_nbr_skills')
    prc_skills = fields.Integer('Percentage of skills', compute='_get_prc_skills')
    skills_daily = fields.Char('Skills', compute='_get_skills_daily')
    
    @api.one
    def _get_skills_daily(self):
        a = unicode([
            { "tooltip" : "Old", "value": 5},
            { "tooltip" : "New", "value": 7},
            { "tooltip" : "New 2", "value": 7},
            { "tooltip" : "New 3", "value": 7},
        ]).replace("'","\"")
        print a
        self.skills_daily = a
        
    @api.one
    def _get_nbr_skills(self):
        self.nbr_skills = len(self.learn_ids)
            
    @api.one
    @api.depends('learn_ids')
    def _get_prc_skills(self):
        nbr = self.env['academy.learning'].search_count([])
        if not nbr:
            self.prc_skills = 0.0
        else:
            self.prc_skills = 100.0 * len(self.learn_ids) / nbr
            
    @api.multi
    def skills_list(self):
        return {
            'name': 'Prof skills',
            'view_type': 'form',
            'view_mode': 'kanban,tree,form',
            'res_model': 'academy.learning',
            'type': 'ir.actions.act_window',
            #'domain': [['proflearn_ids.professor_id', '=', self.id]]
            'domain': [['id', 'in', self.learn_ids.ids]],
        }
    
    @api.multi
    def skills_m2o_list(self):
        return {
            'name': 'Prof skills',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'academy.proflearn',
            'type': 'ir.actions.act_window',
            'domain': [['professor_id', '=', self.id]],
            'context': {'default_professor_id': self.id},
        }
            
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

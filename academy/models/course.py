# -*- coding: utf-8 -*-

from openerp import models, fields, api

class academy(models.Model):
    _name = 'academy.course'

    name = fields.Char(required=True, string="Title")
    description = fields.Text()
    responsible_id = fields.Many2one('res.users')
    session_ids = fields.One2many('academy.session', 'course_id', readonly=True)
    
        
    
class session(models.Model):
    
    _name = 'academy.session'
    
    name = fields.Char()
    end_date = fields.Date()
    begin_date = fields.Date()
    instructor_id = fields.Many2one('res.partner')
    course_id = fields.Many2one('academy.course')
    attendee_ids = fields.Many2many('res.partner')
    
    
class res_partner(models.Model):
    
    _inherit = 'res.partner'
    
    session_ids = fields.Many2many('academy.session')
    
    
class billable_course(models.Model):
    _inherit = 'academy.course'

    product_id = fields.Many2one("product.template", string="Product")
    
    
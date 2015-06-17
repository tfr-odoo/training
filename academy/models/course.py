# -*- coding: utf-8 -*-

from openerp import models, fields, api

class academy(models.Model):
    _name = 'academy.course'
    
    _inherit = 'mail.thread'

    def _default_user(self):
        return self.env.user 
    
    name = fields.Char(required=True, string="Title", translate=True)
    description = fields.Text(copy=False)
    responsible_id = fields.Many2one('res.users', domain=[('course_id', '=', False)])
    session_ids = fields.One2many('academy.session', 'course_id', readonly=True)
    picture = fields.Binary('picture')
    learn_id = fields.Many2one('academy.learning')
    learn_child_id = fields.Many2one('academy.learning')
    
    _sql_constraints = [
        ('name_description_check',
         'CHECK(name != description)',
         "The title of the course should not be the description"),

        ('name_unique',
         'UNIQUE(name)',
         "The course title must be unique"),
                        
        ('responsible_id_unique',
         'UNIQUE(responsible_id)',
         "A user can be only responsible for one course"),
    ]
    
    @api.one
    def copy(self, default=None):
        default = default or {}
        name = "copy of %s" % self.name.replace("copy of ", "")
        copied_count = self.search_count([('name', '=ilike', name + "%")])
        if copied_count:
            name += "(%s)" % copied_count
        default['name'] = name
        return super(academy, self).copy(default=default)

        
    
    
class res_partner(models.Model):
    
    _inherit = 'res.partner'
    
    session_ids = fields.Many2many('academy.session')
    is_instructor = fields.Boolean(default=False)
  
class res_users(models.Model):
    
    _inherit = 'res.users'

    course_id = fields.Many2one('academy.course', compute='_get_course', 
                                inverse='_set_course', 
                                search='_search_course', domain=[('responsible_id', '=', False)])
    
    @api.one
    def _get_course(self):
        course = self.env['academy.course'].search([('responsible_id', '=', self.id)])  
        self.course_id = course[0] if course else False
        
    @api.one   
    def _set_course(self):
        courses = self.env['academy.course'].search([('responsible_id', '=', self.id)])  
        for course in courses:
            course.responsible_id = False
        if self.course_id:
            self.course_id.responsible_id = self.id 
        
    def _search_course(self, operator, value):
        if operator == '=' and not value:
            courses = self.env['academy.course'].search([('responsible_id', '!=', False)])
            responsibles = [r.responsible_id.id for r in courses]
            return [('id', 'not in', responsibles)]
        #TODO handle case != False   
            
        res = self.env['academy.course'].search([('name', operator, value)])
        return [('id', 'in', [r.responsible_id.id for r in res])]
    
class billable_course(models.Model):
    _inherit = 'academy.course'

    product_id = fields.Many2one("product.template", string="Product")
    
    

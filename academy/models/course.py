# -*- coding: utf-8 -*-

from openerp import models, fields, api, exceptions
import logging

class academy(models.Model):
    _name = 'academy.course'

    def _default_user(self):
        return self.env.user 
    
    name = fields.Char(required=True, string="Title")
    description = fields.Text()
    responsible_id = fields.Many2one('res.users', domain=[('course_id', '=', False)])
    session_ids = fields.One2many('academy.session', 'course_id', readonly=True)

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

        
    
class session(models.Model):
    
    _name = 'academy.session'
    _logger = logging.getLogger(__name__)
    
    name = fields.Char()
    end_date = fields.Date()
    begin_date = fields.Date(default=lambda self: fields.Date.today())
    instructor_id = fields.Many2one('res.partner', domain=['&', ('instructor', '=', True),
                     '|', ('category_id.name', 'ilike', "Level 1"),
                          ('category_id.name', 'ilike', "Level 2")])
    course_id = fields.Many2one('academy.course')
    attendee_ids = fields.Many2many('res.partner')
    
    nb_seats = fields.Integer(default=10)
    percent_seat_taken = fields.Float(compute='_get_percent_seats')
    active = fields.Boolean(default=True)
    level = fields.Selection([(1, 'Beginner'), (2, 'advanced'), (3, 'expert')])

    @api.one
    @api.depends('nb_seats', 'attendee_ids')
    def _get_percent_seats(self):
        self._logger.info(self)
        if self.nb_seats > 0:
            self.percent_seat_taken =  len(self.attendee_ids)  / float(self.nb_seats) * 100
        else:
            self.percent_seat_taken = 0.0
      
    def _get_max_level(self, partner):
        level = []
        for categ in partner.category_id:
            if "Teacher / Level" in categ.name:
                level.append(int(categ.name.split(' ')[-1]))
                
        return max(level) if level else 0
    
    @api.onchange('level')
    def _verify_level(self):
        if self.level and self.instructor_id and self._get_max_level(self.instructor_id) < self.level:
            self.instructor_id = False
            
        domain= []
        if self.level:
            for i in xrange(3, self.level - 1, -1):
                domain.append(('category_id.name', 'ilike', "Teacher / Level %s" % i))
            domain = ['|'] * (len(domain) - 1)  + domain
        domain.append(('is_instructor', '=', True))
        
        
        return {'domain' : {'instructor_id' : domain}}
      
      
      
      
        
    @api.onchange('nb_seats', 'attendee_ids')
    def _verify_valid_seats(self):
        if self.nb_seats < 0:
            self.nb_seats = self._origin.nb_seats
            return {
                'warning': {
                    'title': "Incorrect 'seats' value",
                    'message': "The number of available seats may not be negative",
                },
            }
        if self.nb_seats < len(self.attendee_ids):
            return {
                'warning': {
                    'title': "Too many attendees",
                    'message': "Increase seats or remove excess attendees",
                },
            }
    @api.one
    @api.constrains('instructor_id', 'attendee_ids')
    def _check_instructor_not_in_attendees(self):
        if self.instructor_id and self.instructor_id in self.attendee_ids:
            raise exceptions.ValidationError("A session's instructor can't be an attendee")
    
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
    
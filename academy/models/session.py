# -*- coding: utf-8 -*-

from openerp import models, fields, api, exceptions
import logging
import datetime

class session(models.Model):
    
    _name = 'academy.session'
    _logger = logging.getLogger(__name__)
    
    _order = "duration desc"
    
    name = fields.Char()
    end_date = fields.Date()
    begin_date = fields.Date(default=lambda self: fields.Date.today())
    duration = fields.Integer(compute="_get_duration", inverse="_set_duration", store=True)
    duration_hours = fields.Float(compute="_get_hours")
    instructor_id = fields.Many2one('res.partner', domain=['&', ('instructor', '=', True),
                     '|', ('category_id.name', 'ilike', "Level 1"),
                          ('category_id.name', 'ilike', "Level 2")])
    course_id = fields.Many2one('academy.course')
    attendee_ids = fields.Many2many('res.partner')
    
    nb_seats = fields.Integer(default=10)
    percent_seat_taken = fields.Float(compute='_get_percent_seats')
    active = fields.Boolean(default=True)
    level = fields.Selection([(1, 'Beginner'), (2, 'advanced'), (3, 'expert')])
    attendees_count = fields.Integer(compute='_get_attendee_count', store=True)
    
    color = fields.Integer()
    state = fields.Selection([
         ('draft', "Draft"),
         ('confirmed', "Confirmed"),
         ('done', "Done"),
    ], default='draft')
    
    @api.one
    @api.depends('attendee_ids')
    def _get_attendee_count(self):
        self.attendees_count = len(self.attendee_ids) 
        
    @api.one
    @api.depends('duration', 'end_date', 'begin_date')
    def _get_hours(self):
        self.duration_hours = self.duration * 8
    
    @api.one
    @api.depends('end_date', 'begin_date')
    def _get_duration(self):
        self.duration = 0
        if self.begin_date and self.end_date:
            begin_date = fields.Date.from_string(self.begin_date)
            end_date = fields.Date.from_string(self.end_date)
            self.duration = (end_date - begin_date).days + 1
    
    @api.one
    @api.onchange('durations')
    def _set_duration(self):
        begin_date = fields.Date.from_string(self.begin_date)
        self.end_date = begin_date + datetime.timedelta(days=(self.duration - 1))

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
        
    

    @api.one
    def action_draft(self):
        self.state = 'draft'

    @api.one
    def action_confirm(self):
        self.state = 'confirmed'

    @api.one
    def action_done(self):
        self.state = 'done'
        
    @api.multi
    def export_excel(self):
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'academy.export_excel',
            'target': 'new',
        }

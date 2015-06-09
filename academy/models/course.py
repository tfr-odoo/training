# -*- coding: utf-8 -*-

from openerp import models, fields, api
import logging

class academy(models.Model):
    _name = 'academy.course'

    def _default_user(self):
        return self.env.user 
    
    name = fields.Char(required=True, string="Title")
    description = fields.Text()
    responsible_id = fields.Many2one('res.users', default=_default_user)
    session_ids = fields.One2many('academy.session', 'course_id', readonly=True)

    

        
    
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

    @api.one
    @api.depends('nb_seats', 'attendee_ids')
    def _get_percent_seats(self):
        self._logger.info(self)
        if self.nb_seats > 0:
            self.percent_seat_taken =  len(self.attendee_ids)  / float(self.nb_seats) * 100
        else:
            self.percent_seat_taken = 0.0
      
      
      
      
      
      
        
    @api.onchange('nb_seats', 'attendee_ids')
    def _verify_valid_seats(self):
        if self.nb_seats < 0:
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
    
    
class res_partner(models.Model):
    
    _inherit = 'res.partner'
    
    session_ids = fields.Many2many('academy.session')
    is_instructor = fields.Boolean(default=False)
    




    
    
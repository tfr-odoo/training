# -*- coding: utf-8 -*-

from openerp import models, fields, api, exceptions, _, tools

class sessionanalysis(models.Model):
    _name = "academy.session.analysis"
    _description = "Course and session analysis"
    _order='name'
    _auto = False

    name = fields.Char(string="Title")
    responsible_id = fields.Many2one('res.users', string="responsible")
    begin_date = fields.Date("Begin date")
    duration = fields.Integer("Duration")
    attendees_count = fields.Integer("# attendees")
    country_id = fields.Many2one('res.country')
    
    def init(self, cr):
        #tools.sql.drop_view_if_exists(cr, 'academy_session_analysis')
        cr.execute('''CREATE OR REPLACE VIEW academy_session_analysis AS (
            select sess.id, sess.duration, sess.begin_date, sess.attendees_count, 
            course.name, course.responsible_id, prtn.country_id
            from academy_session as sess
            left join academy_course as course on course.id=sess.course_id
            left join res_partner as prtn on prtn.id=course.responsible_id)''')
        
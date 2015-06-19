# -*- coding: utf-8 -*-
from openerp import http

class Academy(http.Controller):
    
    @http.route('/academy/<model("academy.professor"):teacher>/', auth='public', website=True)
    def prof(self, teacher):
        return http.request.render('academy.prof',
            { 'teacher': teacher, 
        })
        
#     @http.route('/academy/academy/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('academy.listing', {
#             'root': '/academy/academy',
#             'objects': http.request.env['academy.academy'].search([]),
#         })

#     @http.route('/academy/academy/objects/<model("academy.academy"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('academy.object', {
#             'object': obj
#         })
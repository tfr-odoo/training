# -*- coding: utf-8 -*-

from openerp import api, models

class ReportSessionSiewSelSessions(models.AbstractModel):
    _name = 'report.academy.report_session_view_selsessions'
    
    @api.multi
    def render_html(self, data=None):
        sessions = self.env['academy.session'].search([('attendees_count', '>=', 3)])
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('academy.report_session_view_selsessions')
        docargs = {
            'doc_ids': sessions._ids,
            'doc_model': report.model,
            'docs': sessions,
        }
        return report_obj.render('academy.report_session_view_selsessions', docargs)
'''
Created on 11 juin 2015

@author: odoo
'''



from openerp import models, fields, api, exceptions

import xlsxwriter
import StringIO
import base64

class session(models.TransientModel):
    _name = 'academy.export_excel'
    
    def _get_default_session(self):
        return self._context.get('active_id')
    
    def _get_default_file_name(self):
        if self._context.get('active_id'):
            return self.env['academy.session'].browse(self._context.get('active_id')).name
        else:
            return ''
    
    session_id = fields.Many2one('academy.session', default=_get_default_session)
    #, default=_get_default_session)
    file_name = fields.Char(default=_get_default_file_name)
    file_data = fields.Binary()
    state = fields.Selection([('step_1', 'Step 1'), ('step_2', 'Step 2')], default='step_1')
    
    HEADER = ['.id', 'name', 'email', 'phone', 'country_id/name', 'country_id/code']
    
    def _set_file_name(self):
        if not self.file_name.endswith(".xlsx"):
            self.file_name = self.file_name + ".xlsx"
    @api.multi
    def generate_file(self):
        self.state = 'step_2'
        self._set_file_name()
            
            
        result = self.session_id.attendee_ids.export_data(self.HEADER)
        
        out = self._write_xlsx(self.HEADER, result.get('datas', [[]]))
        self.file_data = base64.encodestring(out.getvalue())
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'academy.export_excel',
            'target': 'new',
            'res_id' : self.id
        }
        
    def _write_xlsx(self, header, data):
        output = StringIO.StringIO()
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet()
        worksheet.write_row('A' + str(1), header)
        for i, row in enumerate(data):
            worksheet.write_row('A' + str(i+2), row)
        workbook.close()
        return output
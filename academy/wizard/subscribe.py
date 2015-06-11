from openerp import models, fields, api

class Wizard(models.TransientModel):
    _name = 'academy.wizard'

    def _get_sessions(self):
        return self._context.get('active_ids', [])
        
    session_ids = fields.Many2many('academy.session', string="Session", default=_get_sessions)
    attendee_ids = fields.Many2many('res.partner', string="Attendees")
    
    @api.one
    def subscribe(self):
        for session in self.session_ids:
            session.attendee_ids |= self.attendee_ids

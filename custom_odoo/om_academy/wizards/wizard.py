from odoo import models, fields, api, exceptions, _

class Wizard(models.TransientModel):
    _name = 'academy.wizard'
    _description = "Wizard: Quick Registration of Attendees to Sessions"

    def _default_session(self):
        return self.env['academy.wizard'].browse(self._context.get('active_ids'))

    session_ids = fields.Many2many('academy.session', string="Sessions",
                                   required=True, default=_default_session)

    attendee_ids = fields.Many2many('res.partner', string="Attendees")

    def subscribe(self):
        for session in self.session_ids:
            session.attendee_ids |= self.attendee_ids
        return {}

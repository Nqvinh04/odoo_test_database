from datetime import timedelta

from odoo import models, fields, api, exceptions, _


class Session(models.Model):
    _name = 'academy.session'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Academy Session'

    name = fields.Char(required=True, track_visibility='always')
    start_date = fields.Date(default=fields.Date.today)
    duration = fields.Float(digits=(6,2), help="Duration in days")
    seats = fields.Integer(string="Number of seats")
    active = fields.Boolean()
    color = fields.Integer()
    instructor_id = fields.Many2one('res.partner', string="Instructor", track_visibility='always')
    course_id = fields.Many2one('academy.course', ondelete='cascade',
                                string="Course", required=True, track_visibility='always')
    attendee_ids = fields.Many2many('res.partner', string='Attendee')
    taken_seats = fields.Float(string="Taken seats", compute='_taken_seats')
    end_date = fields.Date(string="End Date", store=True,
                           compute='_get_end_date', inverse='_set_end_date')

    attendees_count = fields.Integer(string="Attendees count", compute='_get_attendees_count', store=True)

    @api.depends('seats', 'attendee_ids')
    def _taken_seats(self):
        for r in self:
            if not r.seats:
                r.taken_seats = 0.0
            else:
                r.taken_seats = 100.0 * len(r.attendee_ids) / r.seats

    @api.onchange('seats', 'attendee_ids')
    def _verify_valid_seats(self):
        if self.seats < 0:
            return {
                'warning': {
                    'title': _("Incorrect 'seats' value"),
                    'message': _("The number of available seats may not be negative"),
                },
            }

        if self.seats < len(self.attendee_ids):
            return {
                'warning': {
                    'title': _("Too many Attendees"),
                    'message': _("Increase seats or remove excess attendees"),
                }
            }

    @api.depends('start_date', 'duration')
    def _get_end_date(self):
        for r in self:
            if not (r.start_date and r.duration):
                r.end_date = r.start_date
                continue
            duration = timedelta(days=r.duration, seconds=-1)
            r.end_date = r.start_date + duration

    def _set_end_date(self):
        for r in self:
            if not (r.start_date and r.end_date):
                continue
            r.duration = (r.end_date - r.start_date).days + 1

    @api.constrains('instructor_id', 'attendee_ids')
    def _check_instructor_not_in_attendees(self):
        for r in self:
            if r.instructor_id and r.instructor_id in r.attendee_ids:
                raise exceptions.ValidationError("A session's instructor can't be an attendee")

    @api.depends('attendee_ids')
    def _get_attendees_count(self):
        for r in self:
            r.attendees_count = len(r.attendee_ids)
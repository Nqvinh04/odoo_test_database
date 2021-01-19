from odoo import models, fields, api, _


class Course(models.Model):
    _name = "academy.course"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Academy Course"

    name = fields.Char(string="Title", required=True, track_visibility='always')
    description = fields.Text(string="Description", required=True)
    responsible_id = fields.Many2one('res.users', ondelete='set null',
                                     string="responsible", index=True, track_visibility='always')
    session_ids = fields.One2many('academy.session', 'course_id', string='Session', track_visibility='always')

    def copy(self, default=None):
        default = dict(default or {})
        copied_count = self.search_count(
            [('name', '=like', _(u"Copy of {}%").format(self.name))]
        )
        if not copied_count:
            new_name = _(u"Copy of {}").format(self.name)
        else:
            new_name = _(u"Copy of {} ({})").format(self.name, copied_count)
        default['name'] = new_name
        return super(Course, self).copy(default)

    _sql_constraints = [
        ('name_description_check',
         'CHECK(name != description)',
         "The title of the course should not be the description"),

        ('name_unique',
         'UNIQUE(name)',
         "The course title must be unique"),
    ]


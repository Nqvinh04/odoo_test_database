# -*- coding: utf-8 -*-
{
    'name': "Academy",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Vinh PL",
    'website': "http://www.yourcompany.com",
    'category': 'Extra Tools',
    'version': '0.1',
    'depends': ['base'],
    'data': [
        # 'security/security.xml',
        'security/ir.model.access.csv',
        'views/academy_course.xml',
        'views/academy_session.xml',
        'views/partner.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
    ],
    'installable': True,
    'application': True,
    'auto_install': False,

}


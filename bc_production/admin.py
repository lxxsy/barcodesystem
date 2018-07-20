import xadmin
from .models import *
from xadmin.layout import Main, Tab, Fieldset, Row, TabHolder, AppendedText, Side, Field, Col


class Todayworks(object):
    style = 'table'
    model = Todaywork
    extra = 1


class ScjhbXadmin(object):
    list_display = ['spl', 'rq', 'cpid', 'bc']
    search_fields = ['spl']
    form_layout = (
        Fieldset('',
            Row('spl', 'rq'),
            Row('sl', 'cs'),
            Row('dw', 'bz'),
            Row('bc', 'zt'),
            Row('cpid', 'jybg'),
            css_class='unsort no_title'
        ),
    )
    inlines = [Todayworks, ]
    add_form_template = 'bc_production/production_add.html'
xadmin.site.register(Scjhb, ScjhbXadmin)

import xadmin
from .models import *
from xadmin.layout import Fieldset, Row


class CpmlXadmin(object):
    list_display = ['cpid', 'cpmc', 'pbbh', 'tempname']
    search_fields = ['cpid', 'cpmc']
    form_layout = (
        Fieldset('',
                 Row('cpid', 'cpmc'),
                 Row('cpgg', 'dz'),
                 Row('xkz', 'pw'),
                 Row('bz', 'gg'),
                 Row('cpsx', 'cpxx'),
                 Row('zbq', 'cctj'),
                 Row('tempname', 'sptm'),
                 Row('cpsb', 'cptp'),
                 Row('pbbh'),
                 css_class='unsort no_title'
                 ),
    )
xadmin.site.register(Cpml, CpmlXadmin)

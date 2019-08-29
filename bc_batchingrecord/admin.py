'''
import xadmin
from .models import *
from xadmin.layout import Main, Tab, Fieldset, Row, TabHolder, AppendedText, Side, Field, Col


class Plnote_MainXadmin(object):
    list_display = ['plid']
    search_fields = ['plid']


xadmin.site.register(Plnote_Main, Plnote_MainXadmin)
'''



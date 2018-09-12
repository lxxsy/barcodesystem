import xadmin
from .models import *
from xadmin.layout import Main, Tab, Fieldset, Row, TabHolder, AppendedText, Side, Field, Col


class YlinfoXadmin(object):
    list_display = ['ylid', 'ylname', 'minsl', 'maxsl', 'zf', 'stockid', 'bz', 'ylzt']
    search_fields = ['ylid', 'ylname']
    form_layout = (
        Fieldset('',
            Row('ylid', 'ylname'),
            Row('dw', 'piedw'),
            Row('zbq', 'goodzbq'),
            Row('minsl', 'maxsl'),
            Row('park', 'pieprice'),
            Row('tymc', 'ysbz'),
            # Row('maxsl', 'zf'),
            Row('stockid', 'zf'),
            Row('barcode', 'bz'),
            Row('ylzt'),
            css_class='unsort no_title'
        ),
    )
    add_form_template = 'bc_rmaterial/rmaterial_add.html'
    #change_form_template = 'bc_production/production_update.html'


class YlflXadmin(object):
    list_display = ['flid', 'fldm', 'flmc', 'flsm']
    search_fields = ['flid', 'fldm', 'flmc', 'flsm']


class StockinfoXadmin(object):
    list_display = ['stockid', 'stockname']
    search_fields = ['stockid', 'stockname']


xadmin.site.register(Ylinfo, YlinfoXadmin)
xadmin.site.register(Ylfl, YlflXadmin)
xadmin.site.register(Stockinfo, StockinfoXadmin)
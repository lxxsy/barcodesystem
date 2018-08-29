import xadmin
from .models import *
from xadmin.layout import Fieldset, Row


class CpmlXadmin(object):
    list_display = ['cpid', 'cpmc', 'pbbh', 'tempname']
    search_fields = ['cpid', 'cpmc']
    form_layout = (
        Fieldset('',
                 Row('cpid', 'cpmc'),
                 Row('bzgg', 'cpxkz'),
                 Row('bz', 'pw'),
                 Row('cctj', 'gg'),
                 Row('cpsx', 'cpxx'),
                 Row('zczbq', 'zjzbq'),
                 Row('tempname', 'sptm'),
                 Row('cpsb', 'cpsm'),
                 Row('pbbh', 'cpgg'),
                 css_class='unsort no_title'
                 ),
    )
    add_form_template = 'bc_product/product.html'
    change_form_template = 'bc_product/product_bridge.html'


class CprkXadmin(object):
    list_display = ['cpph', 'cpid', 'cpmc', 'bz', 'rkczy']
    search_fields = ['cpph', 'cpid']
    form_layout = (
        Fieldset('',
                 Row('cpph', 'cpid'),
                 Row('cpmc', 'rkdate'),
                 Row('rksl', 'bz'),
                 Row('rkczy', 'rklxid'),
                ),
    )

xadmin.site.register(Cpml, CpmlXadmin)
xadmin.site.register(Cprk, CprkXadmin)

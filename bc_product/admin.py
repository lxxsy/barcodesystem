import xadmin
from .models import *
from xadmin.layout import Fieldset, Row


class CpmlXadmin(object):
    list_display = ['cpid', 'cpmc', 'pbbh', 'gg']
    search_fields = ['cpid', 'cpmc']
    form_layout = (
        Fieldset('',
                 Row('cpid', 'cpmc'),
                 Row('gg', 'dbz'),
                 Row('pw', 'bz'),
                 Row('cpxkz', 'zbq'),
                 Row('cpsx', 'cpxx'),
                 Row('pbbh', 'cctj'),
                 Row('cpsb', 'cppic'),
                 Row('tempname', 'cpsm'),
                 css_class='unsort no_title'
                 ),
    )
    # add_form_template = 'bc_product/product.html'
    # add_form_template = 'bc_product/aaa.html'
    # change_form_template = 'bc_product/product_bridge.html'


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
# xadmin.site.register(Cprk, CprkXadmin)

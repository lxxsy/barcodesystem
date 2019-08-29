import xadmin
from .models import *
from xadmin.layout import Fieldset, Row


class CpmlXadmin(object):
    list_display = ['cpid', 'cpmc', 'pbbh', 'gg']
    search_fields = ['cpid', 'cpmc']
    add_form_template = 'bc_product/product_add.html'
    change_form_template = 'bc_product/product_update.html'
    remove_permissions = ['delete']
    # 列表页列表显示使用的模板
    # object_list_template = 'bc_rmaterial/stockinfo_list.html'


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

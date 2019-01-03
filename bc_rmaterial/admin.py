import xadmin
from .models import *
from xadmin.layout import Main, Tab, Fieldset, Row, TabHolder, AppendedText, Side, Field, Col


class YlinfoXadmin(object):
    list_display = ['ylid', 'ylname', 'minsl', 'maxsl', 'zf', 'stockid', 'bz', 'ylzt']
    search_fields = ['ylid', 'ylname']
    list_per_page = 10
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
    change_form_template = 'bc_rmaterial/rmaterial_update.html'


class YlflXadmin(object):
    list_display = ['flid', 'fldm', 'flmc', 'flsm']
    search_fields = ['flid', 'fldm', 'flmc', 'flsm']


class StockinfoXadmin(object):
    list_display = ['stockid', 'stockname']
    search_fields = ['stockid', 'stockname']
    # grid_layouts = ['thumbnails', 'table']  内置列表页面以表格形式显示或以单元块显示
    object_list_template = 'bc_rmaterial/stockinfo_list.html'


class GysXadmin(object):
    list_display = ['gyscode', 'gysname', 'addr', 'tel']
    search_fields = ['gyscode', 'gysname']
    add_form_template = 'bc_rmaterial/gys_add.html'
    change_form_template = 'bc_rmaterial/gys_update.html'


class YlinfoHGMLXadmin(object):
    list_display = ['ylid', 'ylname', 'gyscode', 'gysname', 'bz']
    search_fields = ['ylid', 'ylname', 'gyscode', 'gysname']
    add_form_template = 'bc_rmaterial/ylinfo_hgml_add.html'
    change_form_template = 'bc_rmaterial/ylinfo_hgml_update.html'


class EnterstockXadmin(object):
    list_display = ['ylid', 'ylname', 'gyscode', 'gysname', 'barcode', 'zl', 'bz']
    search_fields = ['ylid', 'ylname', 'gyscode', 'gysname']
    add_form_template = 'bc_rmaterial/enterstock_add.html'
    change_form_template = 'bc_rmaterial/enterstock_update.html'
    remove_permissions = ['delete']  # 在列表页上禁用的功能，默认为空，可选项为视图view，增加add，修改change 删除delete


xadmin.site.register(Ylinfo, YlinfoXadmin)
xadmin.site.register(Ylfl, YlflXadmin)
xadmin.site.register(Stockinfo, StockinfoXadmin)
xadmin.site.register(Gys, GysXadmin)
xadmin.site.register(Ylinfo_HGML, YlinfoHGMLXadmin)
xadmin.site.register(Enterstock, EnterstockXadmin)
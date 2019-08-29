import xadmin
from .models import *
from xadmin.layout import Main, Tab, Fieldset, Row, TabHolder, AppendedText, Side, Field, Col


# 原料基础信息配置
class YlinfoXadmin(object):
    # 设置要显示在列表中的字段
    list_display = ['ylid', 'ylname', 'minsl', 'maxsl', 'zf', 'stockid', 'bz', 'ylzt']
    # 列表页搜索框可用于模糊匹配的字段
    search_fields = ['ylid', 'ylname']
    # 设置每页显示多少条记录，默认是100条
    list_per_page = 10
    # 设置表单输入框一行并排几个
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
    # 添加页面使用的模板 默认为 xadmin/views/model_form.html
    add_form_template = 'bc_rmaterial/rmaterial_add.html'
    # 修改页面使用的模板 默认为 xadmin/views/model_form.html
    change_form_template = 'bc_rmaterial/rmaterial_update.html'


# 原料分类信息配置
class YlflXadmin(object):
    list_display = ['flid', 'fldm', 'flmc', 'flsm']
    search_fields = ['flid', 'fldm', 'flmc', 'flsm']


# 原料仓库信息配置
class StockinfoXadmin(object):
    list_display = ['stockid', 'stockname']
    search_fields = ['stockid', 'stockname']
    # grid_layouts = ['thumbnails', 'table']  内置列表页面以表格形式显示或以单元块显示
    # 列表页列表显示使用的模板
    object_list_template = 'bc_rmaterial/stockinfo_list.html'


# 供应商信息配置
class GysXadmin(object):
    list_display = ['gyscode', 'gysname', 'addr', 'tel']
    search_fields = ['gyscode', 'gysname']
    add_form_template = 'bc_rmaterial/gys_add.html'
    change_form_template = 'bc_rmaterial/gys_update.html'


# 合格供应商信息配置
class YlinfoHGMLXadmin(object):
    list_display = ['ylid', 'ylname', 'gyscode', 'gysname', 'bz']
    search_fields = ['ylid', 'ylname', 'gyscode', 'gysname']
    add_form_template = 'bc_rmaterial/ylinfo_hgml_add.html'
    change_form_template = 'bc_rmaterial/ylinfo_hgml_update.html'


# 原料入库信息配置
class EnterstockXadmin(object):
    list_display = ['ylid', 'ylname', 'gyscode', 'gysname', 'barcode', 'zl', 'bz']
    search_fields = ['ylid', 'ylname', 'gyscode', 'gysname']
    add_form_template = 'bc_rmaterial/enterstock_add.html'
    change_form_template = 'bc_rmaterial/enterstock_update.html'
    # 在列表页上禁用的功能，默认为空，可选项为视图view，增加add，修改change 删除delete
    remove_permissions = ['delete']


xadmin.site.register(Ylinfo, YlinfoXadmin)
xadmin.site.register(Ylfl, YlflXadmin)
xadmin.site.register(Stockinfo, StockinfoXadmin)
xadmin.site.register(Gys, GysXadmin)
xadmin.site.register(Ylinfo_HGML, YlinfoHGMLXadmin)
xadmin.site.register(Enterstock, EnterstockXadmin)
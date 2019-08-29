import xadmin
from xadmin.views import BaseAdminView, CommAdminView
from xadmin.layout import Main, Tab, Fieldset, Row, TabHolder, AppendedText, Side, Field, Col
from .models import *


class ThemeXadmin(object):
    enable_themes = True
    use_bootswatch = True


# 后台名称，可更改名称
class GlobalSettings(object):
    site_title = "后台管理系统"
    site_footer = "后台管理系统"
    menu_style = "accordion"


xadmin.site.register(CommAdminView, GlobalSettings)


class Pbfs(object):
    style ='table'  # 属性设置为表格，那么在嵌套关联中会以表格的形式展现
    model = Pbf
    extra = 1


class PbXadmin(object):
    # remove_permissions = ['add', 'change', 'delete']
    list_display = ['pbbh', 'pbname', 'pftype', 'bz', 'yx']
    search_fields = ['pbbh', 'pbname']
    form_layout = (
        Fieldset('',
            Row('pbbh', 'pbname'),
            Row('pftype', 'scsx'),
            Row('scxh', 'bz'),
            Row('yx'),
            css_class='unsort no_title'
        ),
    )
    inlines = [Pbfs, ]
    add_form_template = 'bc_formula/formula_add.html'
    change_form_template = 'bc_formula/formula_update.html'
    # fields = ('pbbh', 'pbname', 'pftype') # 填加数据或者查看数据时，可以设置显示的字段


xadmin.site.register(Pb, PbXadmin)
xadmin.site.register(BaseAdminView, ThemeXadmin)
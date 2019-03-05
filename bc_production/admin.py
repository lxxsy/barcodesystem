import xadmin
from .models import *
from xadmin.layout import Main, Tab, Fieldset, Row, TabHolder, AppendedText, Side, Field, Col


class Todayworks(object):
    style = 'table'
    model = Todaywork
    extra = 1


class ScjhbXadmin(object):
    list_display = ['spl', 'scrq', 'cpid', 'bc']
    search_fields = ['spl']

    form_layout = (
        Fieldset('',
            Row('spl', 'scrq'),
            Row('cpid', 'sl'),
            Row('cs', 'dw'),
            Row('bc', 'bz'),
            Row('zt'),
            css_class='unsort no_title'
        ),
    )
    inlines = [Todayworks, ]
    add_form_template = 'bc_production/production_add.html'
    change_form_template = 'bc_production/production_update.html'
    remove_permissions = ['delete']  # 在列表页上禁用的功能，默认为空，可选项为视图view，增加add，修改change 删除delete


xadmin.site.register(Scjhb, ScjhbXadmin)

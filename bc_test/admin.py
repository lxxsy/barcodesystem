import xadmin
from .models import *
from xadmin.layout import Main, Tab, Fieldset, Row, TabHolder, AppendedText, Side, Field, Col
from bc_rmaterial.models import *

'''
class QypqyXadmin(object):  # 样品取样
    list_display = ['ID', 'ylid', 'cpmc', 'ylpc']
    search_fields = ['ID', 'ylid']
    form_layout = (
        Fieldset('',
            Row('ID', 'cyrq'),
            Row('ylid'),
            Row('cpmc', 'scrq'),
            Row('ylpc', 'gg'),
            Row('cydd', 'cysl'),
            Row('cyjs', 'cyrid'),
            css_class='unsort no_title'
        ),
    )


class Qjybgfs(object):  # 检验报告副表
    style = 'table'
    model = Qjybgf
    extra = 1



class QjybgXadmin(object):  # 检验报告
    list_display = ['bgbh', 'qypqy', 'cpmc', 'pzr']
    search_fields = ['bgbh', 'qypqy']
    form_layout = (
        Fieldset('',
            Row('bgbh', 'qypqy'),
            # Row('qypqy', 'qjybz'),
            Row('cpmc', 'scrq'),
            Row('pzr', 'gg'),
            # Row('cyrq', 'jyyj'),
            # Row('jyjl', 'fl'),
            # Row('pzr', 'shr'),
            # Row('bzr', 'bz'),
            Row('jybgfile', 'bz'),
            css_class='unsort no_title'
        ),
    )
    # inlines = [Qjybgfs, ]


class Qjybzfs(object):  # 检验标准副表
    style = 'table'  # 属性设置为表格，那么在嵌套关联中回忆表格的形式展现
    model = QjybzF
    extra = 1


class QjybzXadmin(object):  # 检验标准
    list_display = ['bzid', 'bzmc', 'zt', 'bz']
    search_fields = ['bzid', 'bzmc']
    form_layout = (
        Fieldset('',
            Row('bzid', 'bzmc'),
            Row('zt', 'bz'),
            css_class='unsort no_title'
        ),
    )
    inlines = [Qjybzfs, ]


class QjcxmXadmin(object):  # 检测项目
    list_display = ['zbmc', 'dw', 'jcffid']
    search_fields = ['zbmc']
    form_layout = (
        Fieldset('',
            Row('zbmc'),
            Row('dw'),
            Row('jcffid'),
            css_class='unsort no_title'
        ),
    )


class QjcffXadmin(object):  # 检测方法
    list_display = ['id', 'jcff', 'jcffdz']
    search_fields = ['id', 'jcff']
    form_layout = (
        Fieldset('',
            Row('id'),
            Row('jcff'),
            Row('jcffdz'),
            css_class='unsort no_title'
        ),
    )
'''

# xadmin.site.register(Qypqy, QypqyXadmin)
# xadmin.site.register(Qjybg, QjybgXadmin)
# xadmin.site.register(Qjybz, QjybzXadmin)
# xadmin.site.register(Qjcxm, QjcxmXadmin)
# xadmin.site.register(Qjcff, QjcffXadmin)

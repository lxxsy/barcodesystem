from django.db import models


class Ylinfo(models.Model):
    ylid = models.CharField(primary_key=True, max_length=50, verbose_name='原料代码')
    ylname = models.CharField(max_length=50, verbose_name='原料名称')
    dw = models.IntegerField(verbose_name='计量单位')  # 1:kg, 2:g,默认kg
    piedw = models.FloatField(verbose_name='单包重量')  # 有提示kg
    zbq = models.IntegerField(blank=True, null=True, default=365, verbose_name='最长质保期')
    goodzbq = models.IntegerField(blank=True, null=True, verbose_name='最佳质保期')
    park = models.IntegerField(blank=True, null=True, verbose_name='仓位')
    pieprice = models.FloatField(blank=True, null=True, verbose_name='单价')
    minsl = models.IntegerField(blank=True, null=True, verbose_name='最小库存')
    maxsl = models.IntegerField(blank=True, null=True, verbose_name='最大库存')
    zf = models.ForeignKey('Ylfl', on_delete=models.CASCADE, verbose_name='分类')
    stockid = models.ForeignKey('Stockinfo', on_delete=models.CASCADE, verbose_name='默认仓库')
    tymc = models.CharField(max_length=30, blank=True, null=True, verbose_name='通用名称')
    ysbz = models.CharField(max_length=50, blank=True, null=True, verbose_name='验收标准号')
    ylzt = models.BooleanField(default=True, verbose_name='可用')  # 默认可用，原料状态(t：可用；f：不可用)
    barcode = models.CharField(max_length=50, blank=True, null=True, verbose_name='原料条形码')  # 针对转盘，自动配外设，当前所使用的原料条码,不显示；
    bz = models.CharField(max_length=200, blank=True, null=True, verbose_name='备注')

    def __str__(self):
        return str(self.ylid)

    class Meta:
        db_table = 'ylinfo'
        verbose_name = '原料'
        verbose_name_plural = '原料基础信息'


class Stockinfo(models.Model):
    stockid = models.CharField(primary_key=True, max_length=20, verbose_name='仓库编号')
    stockname = models.CharField(max_length=50, blank=True, null=True, verbose_name='仓库名称')

    def __str__(self):
        return self.stockname

    class Meta:
        db_table = 'stockinfo'
        verbose_name = '仓库'
        verbose_name_plural = '仓库信息'


class Ylfl(models.Model):
    flid = models.IntegerField(primary_key=True, verbose_name='分类ID')
    fldm = models.CharField(max_length=10, blank=True, null=True, verbose_name='分类代码')
    flmc = models.CharField(max_length=50, blank=True, null=True, verbose_name='名称')
    flsm = models.CharField(max_length=200, blank=True, null=True, verbose_name='说明')

    def __str__(self):
        return self.flmc

    class Meta:
        db_table = 'ylfl'
        verbose_name = '原料分类'
        verbose_name_plural = '原料分类'


class Enterstock(models.Model):
    barcode = models.CharField(max_length=50, verbose_name='原料条码')
    ylid = models.ForeignKey('Ylinfo', on_delete=models.CASCADE, verbose_name='原料代码')
    ylname = models.CharField(max_length=50, verbose_name='原料名称')
    clph = models.CharField(max_length=50, blank=True, null=True, verbose_name='原料批号')
    dbz = models.FloatField(verbose_name='单包重')  # 有提示kg
    zl = models.FloatField(verbose_name='入库重量')
    rdate = models.DateTimeField(verbose_name='入库日期')
    rkck = models.ForeignKey('Stockinfo', on_delete=models.CASCADE, verbose_name='入库仓库')
    scrq = models.DateTimeField(verbose_name='生产日期', blank=True, null=True)
    gyscode = models.CharField(max_length=50, verbose_name='供应商代码')
    gysname = models.CharField(max_length=50, verbose_name='供应商名称')
    lotbar = models.CharField(max_length=50, blank=True, null=True, verbose_name='外部条码')
    bz = models.CharField(max_length=200, blank=True, null=True, verbose_name='备注')
    check1no = models.CharField(max_length=50, verbose_name='检验报告编号')
    pas = models.IntegerField(verbose_name='原料状态')  # 1合格， 0不合格， 2质管放行
    qcmen = models.CharField(max_length=30, blank=True, null=True, verbose_name='检验人')

    def __str__(self):
        return str(self.ylid)

    class Meta:
        db_table = 'enterstock'
        verbose_name = '原料入库'
        verbose_name_plural = '原料入库信息'


class Gys(models.Model):
    gyscode = models.CharField(primary_key=True, max_length=20, verbose_name='供应商代码')
    gysname = models.CharField(max_length=50, verbose_name='供应商名称')
    addr = models.CharField(max_length=60, blank=True, null=True, verbose_name='地址')
    tel = models.CharField(max_length=15, blank=True, null=True, verbose_name='电话')
    fax = models.CharField(max_length=50, blank=True, null=True, verbose_name='传真')
    men = models.CharField(max_length=50, blank=True, null=True, verbose_name='人员')
    email = models.EmailField(max_length=50, blank=True, null=True, verbose_name='邮箱')
    web = models.URLField(max_length=50, blank=True, null=True, verbose_name='网址')
    bz = models.CharField(max_length=200, blank=True, null=True, verbose_name='备注')
    scdz = models.CharField(max_length=50, blank=True, null=True, verbose_name='生产地址')
    yyzzbh = models.CharField(max_length=50, blank=True, null=True, verbose_name='营业执照编号')

    def __str__(self):
        return str(self.gyscode)

    class Meta:
        db_table = 'gys'
        verbose_name = '供应商'
        verbose_name_plural = '供应商信息'


class Ylinfo_HGML(models.Model):
    ylid = models.ForeignKey('bc_rmaterial.Ylinfo', on_delete=models.CASCADE, verbose_name='原料代码')  # FK
    ylname = models.CharField(max_length=50, verbose_name='原料名称')
    gyscode = models.ForeignKey('bc_rmaterial.Gys', on_delete=models.CASCADE, verbose_name='供应商代码')  # 供应商信息
    gysname = models.CharField(max_length=50, verbose_name='供应商名称')
    scxkzh = models.CharField(verbose_name='生产许可证号', max_length=50, blank=True, null=True)
    cppzwh = models.CharField(verbose_name='产品批准文号', max_length=50, blank=True, null=True)
    cpbzbh = models.CharField(verbose_name='产品标准编号', max_length=50, blank=True, null=True)
    jkcpdjz = models.CharField(verbose_name='进口产品登记证号', max_length=50, blank=True, null=True)
    bz = models.CharField(verbose_name='备注', max_length=200, blank=True, null=True)

    def __str__(self):
        return str(self.ylid)

    class Meta:
        db_table = 'ylinfo_hgml'
        verbose_name = '合格原料供应商'
        verbose_name_plural = '合格原料供应商'


class Stock(models.Model):
    ylid = models.CharField(max_length=50, verbose_name='原料代码')
    ylname = models.CharField(max_length=50, verbose_name='原料名称')
    quantity = models.FloatField(verbose_name='在库数量')
    qcsl = models.FloatField(blank=True, null=True, verbose_name='上期结存')  # 在库数量加减之前，首先把在库数量的值填充到这个字段中
    stockid = models.ForeignKey('Stockinfo', on_delete=models.CASCADE, verbose_name='仓库编号')
    qa_hg = models.FloatField(blank=True, null=True, verbose_name='合格数量')  # 默认为在库数量
    bz = models.CharField(max_length=100, blank=True, null=True, verbose_name='备注')

    class Meta:
        db_table = 'stock'
        verbose_name = '原料结存'
        verbose_name_plural = '原料结存表'

'''
class Ll_Main(models.Model):
    llid = models.CharField(verbose_name='领料单号', primary_key=True, max_length=50)
    spl = models.CharField(verbose_name='计划单号', max_length=50)  # 每当新建一个生产计划时，会将计划单号填充到这个字段
    lldate = models.DateField(verbose_name='领料日期')  # 和生产计划的计划日期一致
    llbm = models.CharField(verbose_name='领料部门', max_length=50, blank=True, null=True)
    llmen = models.CharField(verbose_name='领料人', max_length=50, blank=True, null=True)
    bz = models.CharField(verbose_name='备注', max_length=200, blank=True, null=True)
    sh = models.BooleanField(verbose_name='审核')  # 单选框，默认未选中，选中后才会去原料结存表扣除在库数量
    optionaction = models.CharField(verbose_name='操作人', max_length=50, null=True)

    class Meta:
        db_table = 'll_main'
        verbose_name = '原料出库'
        verbose_name_plural = '原料出库'


class Leavestock(models.Model):
    llid = models.ForeignKey('Ll_Main', on_delete=models.CASCADE, verbose_name='领料单号')
    ylbarcode = models.CharField(max_length=50, verbose_name='原料条形码')
    ylid = models.CharField(verbose_name='原料代码', max_length=50)
    cdate = models.DateField(verbose_name='出库日期')  # 同主表的领料日期一致
    clph = models.CharField(verbose_name='原料批号', max_length=50, blank=True, null=True)
    czl = models.FloatField(verbose_name='出库数量')  # 计算后会得出此数据，理论用量
    bz = models.CharField(verbose_name='备注', max_length=200, blank=True, null=True)
    stockid = models.CharField(verbose_name='仓库编号', max_length=50, blank=True, null=True)
    actionid = models.CharField(verbose_name='出库人', max_length=50, null=True)

    class Meta:
        db_table = 'leavestock'
        verbose_name = '原料出库明细'
        verbose_name_plural = '原料出库明细'
'''


class Llyl(models.Model):
    rq = models.DateTimeField(verbose_name='日期')
    ylid = models.CharField(verbose_name='原料代码', max_length=50)
    ylname = models.CharField(max_length=50, verbose_name='原料名称')
    sl = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='理论用量')
    yllx = models.IntegerField(verbose_name='原料类型', blank=True, null=True)
    stockid = models.CharField(verbose_name='仓库编号', max_length=20, blank=True, null=True)
    zsdzl = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='整数袋重量', blank=True, null=True)
    scxh = models.IntegerField(verbose_name='生产线号', blank=True, null=True)
    bz = models.CharField(verbose_name='备注', max_length=200, blank=True, null=True)
    spl = models.CharField(max_length=20, verbose_name='计划单号', default='')

    class Meta:
        db_table = 'llyl'
        verbose_name = '原料领用计算'
        verbose_name_plural = '原料领用计算'


class SystemParameter(models.Model):
    id = models.CharField(max_length=10, primary_key=True, verbose_name='寻找数据的唯一标识')
    lldh = models.IntegerField(verbose_name='领料单号生成')
    scph = models.IntegerField(verbose_name='生产批号生成', default=None)

    class Meta:
        db_table = 'system_parameter'
        verbose_name = '系统参数'
        verbose_name_plural = '系统参数'










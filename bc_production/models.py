from django.db import models


class Scjhb(models.Model):
    spl = models.CharField(primary_key=True, verbose_name='计划单号', max_length=20)  # 新增 ，关联第三方ERP批号
    scrq = models.DateField(verbose_name='日期')  # 生产计划日期
    cpid = models.ForeignKey('bc_product.Cpml', on_delete=models.CASCADE, verbose_name='产品编号')
    cpname = models.CharField(max_length=50, verbose_name='产品名称')
    sl = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='生产数量')
    cs = models.IntegerField(verbose_name='批次数')  # 生产批次(盘数/锅数/车) 默认1
    dw = models.IntegerField(verbose_name='单位')  # 1:kg，2:g 默认kg
    bc = models.IntegerField(verbose_name='班次', blank=True, null=True)
    xdr = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name='下单人')
    zt = models.BooleanField(verbose_name='启用')
    bz = models.CharField(verbose_name='备注', max_length=200, blank=True, null=True)

    def __str__(self):
        return str(self.spl)

    class Meta:
        db_table = 'scjhb'
        verbose_name = '生产计划'
        verbose_name_plural = '生产计划'


class Todaywork(models.Model):  # 生产计划下达后计划明细最少需要一行数据
    ph = models.CharField(verbose_name='生产批号', unique=True, max_length=50)
    spl = models.ForeignKey('Scjhb', on_delete=models.CASCADE, verbose_name='生产单号')
    pldate = models.DateField(verbose_name='计划日期')
    workno = models.IntegerField(verbose_name='生产顺序')
    cpid = models.CharField(verbose_name='产品编号', max_length=50)
    cpname = models.CharField(verbose_name='产品名称', max_length=50)
    pbbh = models.CharField(verbose_name='配方编号', max_length=50)  # 关联产品目录表配方编号
    pbname = models.CharField(verbose_name='配方名称', max_length=50)
    worksl = models.IntegerField(verbose_name='任务次数')  # 默认值1
    plsl = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='数量')  # kg,配料数量（重量）针对比例配方是每锅生产量；比例配方为配方总合
    scxh = models.IntegerField(verbose_name='生产线号', blank=True, null=True)
    bz = models.CharField(verbose_name='备注', max_length=200, blank=True, null=True)
    zt = models.BooleanField(verbose_name='启用')  # 默认为启用

    class Meta:
        db_table = 'todaywork'
        verbose_name = '生产计划明细'
        verbose_name_plural = '生产计划明细'

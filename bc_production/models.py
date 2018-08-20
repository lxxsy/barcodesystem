from django.db import models


class Scjhb(models.Model):
    SCDW = (
        (0, 'kg'),
        (1, 'g'),
    )
    spl = models.CharField(primary_key=True, verbose_name='计划单号', max_length=20)  # 新增 ，关联第三方ERP批号-
    rq = models.DateField(verbose_name='日期')  # 生产计划日期
    cpid = models.ForeignKey('bc_product.Cpml', on_delete=models.CASCADE, verbose_name='产品编号')
    sl = models.FloatField(verbose_name='数量')
    cs = models.IntegerField(verbose_name='批次数', blank=True, null=True)  # 生产批次(盘数/锅数/车)
    dw = models.IntegerField(choices=SCDW, verbose_name='单位', blank=True, null=True)
    zt = models.BooleanField(verbose_name='启用', default=True)
    bz = models.CharField(verbose_name='备注', max_length=50, blank=True, null=True)
    bc = models.IntegerField(verbose_name='班次', blank=True, null=True)

    def __str__(self):
        return self.spl

    class Meta:
        db_table = 'scjhb'
        verbose_name = '生产计划'
        verbose_name_plural = '生产计划'


class Todaywork(models.Model):
    ph = models.CharField(verbose_name='生产批号', primary_key=True, max_length=50)
    spl = models.ForeignKey('Scjhb', on_delete=models.CASCADE, verbose_name='生产单号', max_length=50)
    pldate = models.DateField(verbose_name='计划日期')
    workno = models.IntegerField(verbose_name='生产顺序')
    cpid = models.CharField(verbose_name='产品编号', max_length=50)
    cpname = models.CharField(verbose_name='产品名称', max_length=50)
    pbbh = models.CharField(verbose_name='配方编号', max_length=50)  # 关联产品目录表配方编号
    pbname = models.CharField(verbose_name='配方名称', max_length=50)
    worksl = models.IntegerField(verbose_name='任务次数', default=1)  # 默认值1
    plsl = models.FloatField(verbose_name='数量(kg)', blank=True, null=True)  # 配料数量（重量）针对比例配方是每锅生产量；比例配方为配方总合
    scxh = models.IntegerField(verbose_name='生产线号', blank=True, null=True)
    bz = models.CharField(verbose_name='备注', max_length=100, blank=True, null=True)
    optionid = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name='下单人')  # 关联用户表
    bc = models.IntegerField(verbose_name='班次', blank=True, null=True)
    fwrsx = models.IntegerField(verbose_name='防交叉污染顺序', blank=True, null=True)
    zt = models.BooleanField(verbose_name='启用', default=True)

    class Meta:
        db_table = 'todaywork'
        verbose_name = '生产计划明细'
        verbose_name_plural = '生产计划明细'
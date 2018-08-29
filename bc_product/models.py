from django.db import models


class Cpml(models.Model):
    cpid = models.CharField(primary_key=True, max_length=50, verbose_name='产品编号')
    cpmc = models.CharField(max_length=50, verbose_name='产品名称')
    bzgg = models.CharField(max_length=20, blank=True, null=True, verbose_name='包装规格')
    cpxkz = models.CharField(max_length=50, blank=True, verbose_name='产品许可证')
    pw = models.CharField(max_length=50, blank=True, verbose_name='批准文号')
    bz = models.CharField(max_length=50, blank=True, verbose_name='标准编号')
    pbbh = models.ForeignKey('bc_formula.Pb', on_delete=models.CASCADE, verbose_name='配方编号')
    cpsx = models.IntegerField(blank=True, null=True, verbose_name=' 成品打包上限')
    cpxx = models.IntegerField(blank=True, null=True, verbose_name='成品打包下限')
    gg = models.CharField(max_length=20, blank=True, verbose_name='规格')
    tempname = models.FileField(upload_to='bc_products/cptemp/%Y/%m/%d', verbose_name='成品标签模板')  # (下完计划后，打印标签模板名称)
    zczbq = models.IntegerField(blank=True, null=True, verbose_name='最长质保期(天)')
    zjzbq = models.IntegerField(blank=True, null=True, verbose_name='最佳质保期(天)')  # 用于与todaywork表里的pldate相加生成留样观察记录里的保质截止日期
    cctj = models.CharField(max_length=50, blank=True, null=True, verbose_name='储存条件')
    cpsm = models.FileField(upload_to='bc_products/cpsm/%Y/%m/%d', verbose_name='产品说明')  # 产品说明
    cpgg = models.CharField(max_length=20, verbose_name='产品规格(含量,重量)')  # 产品规格，char(20)（产品的含量、重量等信息）
    cpsb = models.CharField(max_length=50, blank=True, verbose_name='产品商标')  # 产品商标

    def __str__(self):
        return self.cpid

    class Meta:
        db_table = 'cpml'
        verbose_name = '产品'
        verbose_name_plural = '产品目录基础表'


class Cprk(models.Model):
    cpph = models.CharField(verbose_name='成品批号', max_length=50)
    cpid = models.CharField(verbose_name='成品编号', max_length=20)
    cpmc = models.CharField(verbose_name='成品名称', max_length=20)
    rkdate = models.DateTimeField(auto_now_add=True, verbose_name='入库日期')
    rksl = models.IntegerField(verbose_name='入库数量')
    bz = models.CharField(verbose_name='备注', max_length=50, blank=True, null=True)
    rkczy = models.CharField(verbose_name='入库操作员', max_length=50, blank=True, null=True)
    rklxid = models.IntegerField(verbose_name='入库类型ID', blank=True, null=True)

    class Meta:
        db_table = 'cprk'
        verbose_name = '成品'
        verbose_name_plural = '成品入库表'

































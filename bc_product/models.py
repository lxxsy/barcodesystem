from django.db import models


class Cpml(models.Model):
    cpid = models.CharField(primary_key=True, max_length=50, verbose_name='产品编号')
    cpmc = models.CharField(max_length=50, verbose_name='产品名称')
    dz = models.FloatField(blank=True, null=True, verbose_name='包装规格')
    xkz = models.CharField(max_length=50, blank=True, verbose_name='产品许可证')
    pw = models.CharField(max_length=50, blank=True, verbose_name='批准文号')
    bz = models.CharField(max_length=50, blank=True, verbose_name='标准编号')
    pbbh = models.OneToOneField('bc_formula.Pb', on_delete=models.CASCADE, verbose_name='配方编号')
    cpsx = models.FloatField(blank=True, null=True, verbose_name=' 打包上限')
    cpxx = models.FloatField(blank=True, null=True, verbose_name='成品打包下限')
    gg = models.CharField(max_length=20, blank=True, verbose_name='规格')
    tempname = models.CharField(max_length=50, blank=True, null=True, verbose_name='标签模板')  # (下完计划后，打印标签模板名称)
    zbq = models.IntegerField(blank=True, null=True, verbose_name='质保期(天)')  # 用于与todaywork表里的pldate相加生成留样观察记录里的保质截止日期
    cctj = models.CharField(max_length=50, blank=True, null=True, verbose_name='储存条件')  #
    sptm = models.CharField(max_length=20, blank=True, verbose_name='商品条码')  # 如：06901234000016；
    cptp = models.ImageField(upload_to='bc_products', blank=True, verbose_name='产品图片')  # 产品图片信息，单张<2M,
    cpgg = models.CharField(max_length=20, verbose_name='产品规格(含量,重量)')  # 产品规格，char(20)（产品的含量、重量等信息）
    cpsb = models.CharField(max_length=50, blank=True, verbose_name='产品商标')  # 产品商标
    # 5、产品扩展属性字段

    def __str__(self):
        return self.cpid

    class Meta:
        db_table = 'cpml'
        verbose_name = '产品'
        verbose_name_plural = '产品目录基础表'


class Enterstockcp(models.Model):
    cpid = models.ForeignKey('Cpml', models.CASCADE, verbose_name='产品代码')  # FK 产品目录
    lot = models.CharField(verbose_name='批号', max_length=50)
    rdate = models.DateTimeField(auto_now_add=True, verbose_name='入库日期')
    rsl = models.FloatField(verbose_name='入库数量')
    bz = models.CharField(verbose_name='备注', max_length=50, blank=True, null=True)
    actionid = models.CharField(verbose_name='入库操作员账号', max_length=50, blank=True, null=True)
    bar = models.CharField(verbose_name='成品条码', max_length=50, blank=True, null=True)
    rklxid = models.IntegerField(verbose_name='入库类型ID', blank=True, null=True)
    # syl = models.FloatField(verbose_name='剩余量', blank=True, null=True)  # 不显示

    class Meta:
        db_table = 'EnterStockCP'
        verbose_name = '成品'
        verbose_name_plural = '成品入库表'

































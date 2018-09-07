from django.db import models


class Cpml(models.Model):
    cpid = models.CharField(primary_key=True, max_length=50, verbose_name='产品编号')
    cpmc = models.CharField(max_length=50, verbose_name='产品名称')
    gg = models.CharField(max_length=20, blank=True, null=True, verbose_name='规格')
    dbz = models.CharField(max_length=20, blank=True, verbose_name='单包重')
    pw = models.CharField(max_length=50, blank=True, verbose_name='批准文号')
    bz = models.CharField(max_length=50, blank=True, verbose_name='标准编号')
    cpxkz = models.CharField(max_length=50, blank=True, verbose_name='产品许可证')
    pbbh = models.ForeignKey('bc_formula.Pb', on_delete=models.CASCADE, verbose_name='配方编号')
    cpsx = models.IntegerField(blank=True, null=True, verbose_name=' 包装上限')
    cpxx = models.IntegerField(blank=True, null=True, verbose_name='包装下限')
    zbq = models.IntegerField(blank=True, null=True, verbose_name='保质期')  # 表单后面添加天字
    cctj = models.CharField(max_length=50, blank=True, null=True, verbose_name='储存条件')
    cpsb = models.CharField(max_length=50, blank=True, verbose_name='产品商标')
    cppic = models.ImageField(upload_to='bc_products/cppic/%Y/%m/%d', verbose_name='产品图片')
    cpsm = models.FileField(upload_to='bc_products/cpsm/%Y/%m/%d', verbose_name='产品说明')
    tempname = models.FileField(upload_to='bc_products/cptemp/%Y/%m/%d', verbose_name='成品标签模板')  # (下完计划后，打印标签模板名称)

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

































from django.db import models


class Ylinfo(models.Model):
    JLDW = (
        ('0', 'kg'),
        ('1', 'g'),
    )
    ylid = models.CharField(primary_key=True, max_length=50, verbose_name='原料代码')
    ylname = models.CharField(max_length=50, verbose_name='名称')
    dw = models.CharField(default='0', max_length=50, choices=JLDW, verbose_name='计量单位')  # 默认kg
    piedw = models.IntegerField(verbose_name='单包重量(kg)')  # 包装规格
    zczbq = models.IntegerField(default=365, verbose_name='最长质保期(天)')
    zjzbq = models.IntegerField(default=365, verbose_name='最佳质保期(天)')
    park = models.IntegerField(blank=True, null=True, verbose_name='存放仓位(1~60)用于原料指定料桶')
    bz = models.CharField(max_length=100, blank=True, null=True, verbose_name='备注')
    pieprice = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True, verbose_name='单价')
    minsl = models.FloatField(verbose_name='最小库存')
    maxsl = models.FloatField(verbose_name='最大库存')
    zf = models.ForeignKey('Ylfl', on_delete=models.CASCADE, blank=True, null=True, verbose_name='原料分类')  # FK关联原料分类
    stockid = models.ForeignKey('Stockinfo', on_delete=models.CASCADE, blank=True, null=True, verbose_name='默认仓库')  # FK关联仓库基础表
    tymc = models.CharField(max_length=30, blank=True, null=True, verbose_name='通用名称')
    ysbz = models.IntegerField(blank=True, null=True, verbose_name='验收标准号')
    ylzt = models.BooleanField(default=True, verbose_name='原料状态')
    barcode = models.CharField(max_length=50, blank=True, null=True, verbose_name='原料条形码')  # 针对转盘，自动配外设，当前所使用的原料条码,不显示；

    def __str__(self):
        return str(self.ylname)

    class Meta:
        db_table = 'ylinfo'
        verbose_name = '原料'
        verbose_name_plural = '原料基础信息表'


class Stockinfo(models.Model):
    stockid = models.CharField(primary_key=True, max_length=20, verbose_name='仓库编号')
    stockname = models.CharField(max_length=50, blank=True, null=True, verbose_name='仓库名称')

    def __str__(self):
        return self.stockname

    class Meta:
        db_table = 'stockinfo'
        verbose_name = '仓库'
        verbose_name_plural = '仓库基础表'


class Ylfl(models.Model):
    flid = models.IntegerField(primary_key=True, verbose_name='分类编号')
    fldm = models.CharField(max_length=10, blank=True, null=True, verbose_name='分类代码')
    flmc = models.CharField(max_length=50, blank=True, null=True, verbose_name='名称')
    flsm = models.CharField(max_length=200, blank=True, null=True, verbose_name='说明')

    def __str__(self):
        return self.flmc

    class Meta:
        db_table = 'ylfl'
        verbose_name = '原料分类'
        verbose_name_plural = '原料分类基础表'
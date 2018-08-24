from django.db import models
from django.dispatch import receiver
from django.db.models.signals import *

'''
class Qypqy(models.Model):
    ID = models.CharField(primary_key=True, verbose_name='样品编号', max_length=50)
    cyrq = models.DateField(auto_now_add=True, verbose_name='抽样日期')
    ylid = models.ForeignKey('bc_production.Scjhb', on_delete=models.CASCADE, verbose_name='计划单号', max_length=50)  # 原料从[Enterbarcod]取数据，产品从【scjhb】取数据`#
    cpmc = models.CharField(verbose_name='产品名称', max_length=50)
    scrq = models.DateField(verbose_name='生产日期')
    ylpc = models.CharField(verbose_name='产品批号', max_length=50, blank=True, null=True)
    gg = models.CharField(verbose_name='规格', max_length=50, blank=True, null=True)
    cydd = models.CharField(verbose_name='抽样地点', max_length=30, blank=True, null=True)
    cysl = models.CharField(verbose_name='样品数量', max_length=50)  # 如：约500g×2份
    cyjs = models.CharField(verbose_name='抽样基数', max_length=50, blank=True, null=True)  # 如 200kg
    cyrid = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name='抽样人ID')  # 关联用户表

    def __str__(self):
        return self.ID

    class Meta:
        db_table = 'qypqy'
        verbose_name = '样品取样'
        verbose_name_plural = '样品取样'
'''


class Qjybg(models.Model):
    bgbh = models.CharField(verbose_name='报告编号', primary_key=True, max_length=20)
    qypqy = models.OneToOneField('bc_production.Scjhb', on_delete=models.CASCADE, verbose_name='检验批号')
    cpmc = models.CharField(max_length=50, verbose_name='产品名称')
    scrq = models.DateField(verbose_name='生产日期')
    gg = models.CharField(verbose_name='规格', max_length=50, blank=True)
    pzr = models.CharField(verbose_name='批准人', max_length=20, blank=True, null=True)
    bz = models.CharField(verbose_name='备注', max_length=500, blank=True, null=True)
    jybgfile = models.FileField(upload_to='bc_test/jybg/%Y/%m/%d', verbose_name='检验报告文件', null=True)
    # cyrq = models.DateField(verbose_name='抽样日期', blank=True)
    # jyyj = models.CharField(verbose_name='检验依据', max_length=1000, blank=True, null=True)
    # jyjl = models.CharField(verbose_name='检验结论', max_length=1000, blank=True, null=True)
    # fl = models.CharField(verbose_name='分类', choices=JYLB, max_length=20)  # 进厂检验、出厂检验
    # shr = models.CharField(verbose_name='审核人', max_length=20, blank=True, null=True)
    # bzr = models.CharField(verbose_name='制编人', max_length=20, blank=True, null=True)
    # sh = models.BooleanField(verbose_name='审核状态', default=True)
    # qjybz = models.ForeignKey('Qjybz', on_delete=models.CASCADE, verbose_name='检验标准')
    # ylpc = models.CharField(verbose_name='批号', max_length=50)

    def __str__(self):
        return self.bgbh

    class Meta:
        db_table = 'qjybg'
        verbose_name = '检验报告'
        verbose_name_plural = '检验报告'

'''
class Qjybgf(models.Model):
    bgbh = models.ForeignKey('Qjybg', on_delete=models.CASCADE, verbose_name='报告编号')
    jcxm = models.ForeignKey('Qjcxm', on_delete=models.CASCADE, verbose_name='检测项目编号')
    xmname = models.CharField(max_length=20, verbose_name='检测项目名称')
    dw = models.CharField(max_length=20, verbose_name='单位', blank=True)
    bzz = models.DecimalField(max_digits=18, decimal_places=8, verbose_name='标准值', blank=True, null=True)
    pdz = models.DecimalField(max_digits=18, decimal_places=8, verbose_name='判定值', blank=True, null=True)
    jcz = models.DecimalField(max_digits=18, decimal_places=8, verbose_name='检测值', blank=True, null=True)
    jcff = models.CharField(max_length=100, verbose_name='检测方法')
    bz = models.CharField(max_length=200, verbose_name='备注', blank=True)
    pd = models.BooleanField(default=True, verbose_name='是否合格')

    class Meta:
        db_table = 'qjybgf'
        verbose_name = '检验报告副表'
        verbose_name_plural = '检验报告副表'


class Qjybz(models.Model):
    bzid = models.CharField(primary_key=True, verbose_name='检验标准编号', max_length=20)
    bzmc = models.CharField(verbose_name='标准名称', max_length=50)
    zt = models.SmallIntegerField(verbose_name='状态', blank=True, null=True)
    bz = models.CharField(verbose_name='备注', max_length=200, blank=True, null=True)

    def __str__(self):
        return self.bzid

    class Meta:
        db_table = 'qjybz'
        verbose_name = '检验标准'
        verbose_name_plural = '检验标准'


class QjybzF(models.Model):
    bzid = models.ForeignKey('Qjybz', on_delete=models.CASCADE, verbose_name='检验标准主表')
    jcxmid = models.ForeignKey('Qjcxm', on_delete=models.CASCADE, verbose_name='检测项目编号')
    stdlower = models.DecimalField(verbose_name='标准值下限', max_digits=18, decimal_places=8, blank=True, null=True)
    stdupper = models.DecimalField(verbose_name='标准值上限', max_digits=18, decimal_places=8, blank=True, null=True)
    acplower = models.DecimalField(verbose_name='收货值上限', max_digits=18, decimal_places=8, blank=True, null=True)
    acpupper = models.DecimalField(verbose_name='收货值下限', max_digits=18, decimal_places=8, blank=True, null=True)
    bj = models.BooleanField(default=True, verbose_name='必检')

    class Meta:
        db_table = 'qjybzf'
        verbose_name = '检验标准副表'
        verbose_name_plural = '检验标准副表'
        # unique_together = (('bzid', 'jcxmid'),)


class Qjcxm(models.Model):
    zbmc = models.CharField(verbose_name='检测项目名称', max_length=50)
    dw = models.CharField(verbose_name='单位', max_length=50, blank=True)
    jcffid = models.ForeignKey('Qjcff', on_delete=models.CASCADE, verbose_name='检测方法编号', blank=True, null=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'qjcxm'
        verbose_name = '检测项目'
        verbose_name_plural = '检测项目基础表'
'''

'''
class Qjcff(models.Model):
    jcff = models.CharField(verbose_name='检测方法', max_length=100)
    jcffdz = models.FileField(upload_to='bc_test/jcff/%Y/%m/%d', verbose_name='检测方法文件', blank=True, null=True)

    def __str__(self):
        return self.jcff

    class Meta:
        db_table = 'Qjcff'
        verbose_name = '检测方法'
        verbose_name_plural = '检测方法基础表'
'''
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import *


'''
class Cpypqy(models.Model):
    ypbc = models.CharField(primary_key=True, verbose_name='样品编号', max_length=50)
    cyrq = models.DateField(auto_now_add=True, verbose_name='抽样日期')
    ylid = models.ForeignKey('bc_production.Scjhb', on_delete=models.CASCADE, verbose_name='计划单号', max_length=50)
    cpmc = models.CharField(verbose_name='产品名称', max_length=50)  # 自动获取
    scrq = models.DateField(verbose_name='生产日期')  # 自动获取
    cppc = models.CharField(verbose_name='产品生产批号', max_length=50)  # 做复选框，不做外键
    gg = models.CharField(max_length=20, blank=True, verbose_name='规格')
    cydd = models.CharField(verbose_name='抽样地点', max_length=50, blank=True, null=True)
    cysl = models.CharField(verbose_name='样品数量', max_length=50)  # 如：约500g×2份
    cyjs = models.CharField(verbose_name='抽样基数', max_length=50, blank=True, null=True)  # 如 200kg
    cyrid = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name='抽样人')  # 关联用户表

    def __str__(self):
        return self.ypbc

    class Meta:
        db_table = 'cpypqy'
        verbose_name = '样品取样'
        verbose_name_plural = '样品取样'


class CpJybg(models.Model):
    bgbh = models.CharField(verbose_name='检验报告编号', primary_key=True, max_length=20)
    qypqy = models.OneToOneField('Cpypqy', on_delete=models.CASCADE, verbose_name='样品编号')
    ph = models.CharField(verbose_name='批号', max_length=50)  # 自动获取
    cyrq = models.DateField(verbose_name='抽样日期', blank=True)  # 自动获取
    cpmc = models.CharField(max_length=50, verbose_name='产品名称')  # 自动获取
    scrq = models.DateField(verbose_name='生产日期')  # 自动获取
    gg = models.CharField(verbose_name='规格', max_length=50, blank=True)  # 自动获取
    jyyj = models.CharField(verbose_name='检验依据', max_length=500, blank=True, null=True)
    jyjl = models.CharField(verbose_name='检验结论', max_length=500, blank=True, null=True)
    jyr = models.CharField(verbose_name='检验人', max_length=20, blank=True)
    shr = models.CharField(verbose_name='审核人', max_length=20, blank=True)
    pzr = models.CharField(verbose_name='批准人', max_length=20, blank=True)
    qjybz = models.ForeignKey('Qjybz', on_delete=models.CASCADE, verbose_name='检验标准')  # 根据选择的标准自动把此标准选择的检测项目填充到报告副表
    bz = models.CharField(verbose_name='备注', max_length=500, blank=True, null=True)
    jybgfile = models.FileField(upload_to='bc_test/jybg/%Y/%m/%d', verbose_name='检验报告文件')

    def __str__(self):
        return self.bgbh

    class Meta:
        db_table = 'cpjybg'
        verbose_name = '产品检验报告'
        verbose_name_plural = '产品检验报告'


class CpJybgf(models.Model):
    bgbh = models.ForeignKey('CpJybg', on_delete=models.CASCADE, verbose_name='检验报告编号')
    jcxm = models.ForeignKey('Qjcxm', on_delete=models.CASCADE, verbose_name='检测项目编号')
    xmname = models.CharField(max_length=50, verbose_name='检测项目名称')
    dw = models.CharField(max_length=20, verbose_name='单位', blank=True)
    bzz = models.FloatField(verbose_name='标准值', blank=True, null=True)
    pdz = models.FloatField(verbose_name='判定值', blank=True, null=True)
    jcz = models.FloatField(verbose_name='检测值', blank=True, null=True)
    jcff = models.CharField(max_length=50, verbose_name='检测方法')  # 自动获取，根据检测项目的编号获取到检测方法
    bz = models.CharField(max_length=200, verbose_name='备注', blank=True)
    pd = models.BooleanField(default=True, verbose_name='合格')  # 默认为合格

    class Meta:
        db_table = 'cpjybgf'
        verbose_name = '产品检验报告副表'
        verbose_name_plural = '产品检验报告副表'


class Qjybz(models.Model):
    bzid = models.CharField(primary_key=True, verbose_name='检验标准编号', max_length=50)
    bzmc = models.CharField(verbose_name='标准名称', max_length=50)
    bz = models.CharField(verbose_name='备注', max_length=200, blank=True, null=True)

    def __str__(self):
        return self.bzid

    class Meta:
        db_table = 'qjybz'
        verbose_name = '检验标准'
        verbose_name_plural = '检验标准'


class QjybzF(models.Model):
    bzid = models.ForeignKey('Qjybz', on_delete=models.CASCADE, verbose_name='检验标准')
    jcxmid = models.ForeignKey('Qjcxm', on_delete=models.CASCADE, verbose_name='检测项目编号')
    stdlower = models.FloatField(verbose_name='标准值下限', blank=True, null=True)
    stdupper = models.FloatField(verbose_name='标准值上限', blank=True, null=True)
    acplower = models.FloatField(verbose_name='收货值上限', blank=True, null=True)
    acpupper = models.FloatField(verbose_name='收货值下限', blank=True, null=True)
    bj = models.BooleanField(default=True, verbose_name='必检')

    class Meta:
        db_table = 'qjybzf'
        verbose_name = '检验标准副表'
        verbose_name_plural = '检验标准副表'
        # unique_together = (('bzid', 'jcxmid'),)


class Qjcxm(models.Model):
    zbmc = models.CharField(verbose_name='检测项目名称', max_length=50)
    dw = models.CharField(verbose_name='单位', max_length=50, blank=True)
    jcffid = models.ForeignKey('Qjcff', on_delete=models.CASCADE, verbose_name='检测方法编号')

    def __str__(self):
        return self.zbmc

    class Meta:
        db_table = 'qjcxm'
        verbose_name = '检测项目'
        verbose_name_plural = '检测项目基础表'


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
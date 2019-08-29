from django.db import models


# 称量记录主表
class PLNote_Main(models.Model):
    plid = models.CharField(verbose_name='混料编号', primary_key=True, max_length=50)
    pldatetime = models.DateTimeField(verbose_name='混料日期')  # 以前为：YY-MM-DD，可考虑加上时间 H:mm:ss
    pbbh = models.CharField(verbose_name='配方编号', max_length=50)
    actionid = models.CharField(verbose_name='操作员ID', max_length=50)
    mz = models.FloatField(verbose_name='复核毛重', blank=True, null=True)
    pz = models.FloatField(verbose_name='复核皮重', blank=True, null=True)
    dw = models.CharField(verbose_name='单位', max_length=50, blank=True, null=True)
    bc = models.IntegerField(verbose_name='班次', blank=True, null=True)

    class Meta:
        db_table = 'PLNote_Main'
        verbose_name = '配料记录'
        verbose_name_plural = '配料记录'


# 称量记录副表1
class PLNote_fb1(models.Model):
    fplid = models.AutoField(auto_created=True, primary_key=True, verbose_name='ID')
    plid = models.ForeignKey('PLNote_Main', on_delete=models.CASCADE, verbose_name='混料编号')
    plno = models.IntegerField(verbose_name='配料顺序')  # 配料称量顺序号，关联[pbf]表[plno]字段 称量顺序号
    ylid = models.CharField(verbose_name='原料代码', max_length=50)
    ylzl = models.FloatField(verbose_name='称量值')  # 实际称量值，如是称零头，需加整件重量
    llyl = models.FloatField(verbose_name='理论值', blank=True, null=True)  # 配方标准值
    gc = models.CharField(verbose_name=' 公差', max_length=50, blank=True, null=True)
    mz = models.FloatField(verbose_name='毛重', blank=True, null=True)
    pz = models.FloatField(verbose_name='皮重', blank=True, null=True)
    zsd = models.IntegerField(verbose_name='整件数', blank=True, null=True)
    clr = models.CharField(verbose_name='操作称量人', max_length=50, blank=True, null=True)
    ltzl = models.FloatField(verbose_name='零头重量', blank=True, null=True)

    class Meta:
        db_table = 'PLNote_fb1'
        verbose_name = '配料记录'
        verbose_name_plural = '配料记录'


# 称量记录副表2
class PLNote_fb2(models.Model):
    fplid = models.ForeignKey('PLNote_fb1', on_delete=models.CASCADE, verbose_name='配料记录副库ID')  # 关联[PLNote_fb1]表[FPLID]字段
    ylbarcode = models.CharField(verbose_name='原料条形码', max_length=50)  # 关联[Enterstock]表'

    class Meta:
        db_table = 'PLNote_fb2'
        verbose_name = '配料记录'
        verbose_name_plural = '配料记录'

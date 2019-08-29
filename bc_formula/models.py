from django.db import models


class Pb(models.Model):
    pbbh = models.CharField(primary_key=True, max_length=50, verbose_name='配方编号')
    pbname = models.CharField(max_length=50, verbose_name='配方名称')
    pftype = models.CharField(verbose_name='配方类型', max_length=15)  # 0:标准配方， 1:比例配方
    scsx = models.IntegerField(blank=True, null=True, verbose_name='生产顺序')
    scxh = models.IntegerField(blank=True, null=True, verbose_name='默认生产线')  # 1
    yx = models.BooleanField(default=True, verbose_name='有效配方')
    bz = models.CharField(max_length=300, blank=True, null=True, verbose_name='备注')
    validity = models.BooleanField(default=False, verbose_name='有无产品')  # 产品与配方一对一关系，如配方有了对应的产品，则改为True

    def __str__(self):
        return str(self.pbbh)

    class Meta:
        db_table = 'pb'
        verbose_name = '配方'
        verbose_name_plural = '配方信息'


class Pbf(models.Model):
    pbbh = models.ForeignKey('Pb', on_delete=models.CASCADE, verbose_name='配方编号')  # 关联配方主表
    plno = models.IntegerField(verbose_name='序号')
    ylid = models.ForeignKey('bc_rmaterial.Ylinfo', on_delete=models.CASCADE, verbose_name='原料代码')  # 关联的原料删除不影响此数据
    ylname = models.CharField(max_length=50, verbose_name='原料名称')
    bzgl = models.FloatField(verbose_name='标准值')
    topz = models.FloatField(verbose_name='上限', blank=True, null=True)
    lowz = models.FloatField(verbose_name='下限', blank=True, null=True)
    dw = models.CharField(verbose_name='单位', max_length=20)  # 默认kg
    jno = models.IntegerField(verbose_name='投料顺序')  # 默认原料分类ID;
    lt = models.BooleanField(default=True, verbose_name='称零头')
    zs = models.BooleanField(default=True, verbose_name='追溯')

    def __str__(self):
        return str(self.pbbh)

    class Meta:
        db_table = 'pbf'
        verbose_name = '配方明细'
        verbose_name_plural = '配方明细'



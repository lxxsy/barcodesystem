from django.db import models


class Pb(models.Model):
    PFLX = (
        ('ONE', '标准配方'),
        ('TWO', '比例配方'),
    )
    pbbh = models.CharField(primary_key=True, max_length=50, verbose_name='配方编号')
    pbname = models.CharField(max_length=50, verbose_name='配方名称')
    pftype = models.CharField(max_length=15, choices=PFLX, default='ONE', verbose_name='配方类型')
    scsx = models.IntegerField(blank=True, null=True, verbose_name='生产顺序')
    scxh = models.IntegerField(blank=True, null=True, default=1, verbose_name='默认生产线')
    yx = models.BooleanField(default=True, verbose_name='有效配方')
    bz = models.CharField(max_length=220, blank=True, null=True, verbose_name='备注')

    def __str__(self):
        return self.pbbh

    class Meta:
        db_table = 'pb'
        verbose_name = '配方'
        verbose_name_plural = '配方'


class Pbf(models.Model):
    JLDW = (
        ('ONE', 'kg'),
        ('TWO', 'g'),
    )
    pbbh = models.ForeignKey('Pb', on_delete=models.CASCADE, verbose_name='配方编号')  # 关联配方主表
    plno = models.IntegerField(verbose_name='序号')
    ylid = models.ForeignKey('bc_rmaterial.Ylinfo', on_delete=models.CASCADE, verbose_name='原料代码')
    bzgl = models.FloatField(verbose_name='标准值')
    topz = models.FloatField(verbose_name='上限')
    lowz = models.FloatField(verbose_name='下限')
    dw = models.CharField(max_length=20, choices=JLDW, default='ONE', verbose_name='单位')
    jno = models.IntegerField(verbose_name='投料顺序')
    lt = models.BooleanField(default=True, verbose_name='称零头')
    zs = models.BooleanField(default=True, verbose_name='追溯')

    class Meta:
        db_table = 'pbf'
        verbose_name = '配方副表'
        verbose_name_plural = '配方副表'



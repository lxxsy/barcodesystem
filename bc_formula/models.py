from django.db import models


class Pb(models.Model):
    PFLX = (
        (0, '标准配方'),
        (1, '比例配方'),
    )
    pbbh = models.CharField(primary_key=True, max_length=50, verbose_name='配方编号')
    pbname = models.CharField(max_length=50, blank=True, null=True, verbose_name='配方名称')
    pftype = models.IntegerField(blank=True, null=True, choices=PFLX, default=0, verbose_name='配方类型(0：标准配方；1：比例配方)')
    shr = models.CharField(max_length=50, blank=True, null=True, verbose_name='审核人')
    fwrsx = models.IntegerField(blank=True, null=True, verbose_name='防交叉污染生产顺序')
    scxh = models.IntegerField(blank=True, null=True, verbose_name='默认生产线')
    pfsj = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name='配方建立日期')
    sh = models.BooleanField(default=True, verbose_name='审核状态')
    bz = models.CharField(max_length=220, blank=True, null=True, verbose_name='备注')
    yx = models.BooleanField(default=True, verbose_name='有效配方')

    def __str__(self):
        return self.pbbh

    class Meta:
        db_table = 'pb'
        verbose_name = '配方'
        verbose_name_plural = '配方'


class Pbf(models.Model):
    JLDW = (
        ('0', 'kg'),
        ('1', 'g'),
    )
    pbbh = models.ForeignKey('Pb', on_delete=models.CASCADE, verbose_name='配方编号(与主表关联)')  # 关联配方主表
    plno = models.SmallIntegerField(verbose_name='称量顺序号')
    ylid = models.ForeignKey('bc_rmaterial.Ylinfo', on_delete=models.CASCADE, verbose_name='原料代码')
    bzgl = models.FloatField(verbose_name='标准值')
    topz = models.FloatField(verbose_name='上限值')
    lowz = models.FloatField(verbose_name='下限值')
    dw = models.CharField(max_length=20, blank=True, null=True, choices=JLDW, default='0', verbose_name='单位  ')
    cno = models.IntegerField(blank=True, null=True, verbose_name='使用电子秤端口号')
    jno = models.IntegerField(verbose_name='加料顺序')
    lt = models.BooleanField(default=True, verbose_name='称零头')
    zsxs = models.BooleanField(default=True, verbose_name='外部追溯显示')

    class Meta:
        db_table = 'pbf'
        verbose_name = '配方副表'
        verbose_name_plural = '配方副表'



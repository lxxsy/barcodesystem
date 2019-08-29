from django.db import models
import os
import uuid


# 存储图片时，进行一次分类判断
def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    ext = filename.split('.')[-1]
    # filename = '{}.{}'.format(uuid.uuid4().hex[:8], ext)
    sub_folder = 'grf'
    if ext.lower() in ["jpg", "png", "gif"]:
        sub_folder = "picture"
    elif ext.lower() not in ["grf"]:
        sub_folder = "document"
    return os.path.join(str(instance.user.id), sub_folder, filename)


class Cpml(models.Model):
    cpid = models.CharField(primary_key=True, max_length=50, verbose_name='产品编号')
    cpmc = models.CharField(max_length=50, verbose_name='产品名称')
    gg = models.CharField(max_length=20, blank=True, null=True, verbose_name='规格')
    dbz = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True, verbose_name='单包重')
    pw = models.CharField(max_length=50, blank=True, null=True, verbose_name='批准文号')
    bz = models.CharField(max_length=50, blank=True, null=True, verbose_name='标准编号')
    cpxkz = models.CharField(max_length=50, blank=True, null=True, verbose_name='产品许可证')
    pbbh = models.OneToOneField('bc_formula.Pb', on_delete=models.CASCADE, verbose_name='配方编号')
    cpsx = models.FloatField(blank=True, null=True, verbose_name=' 包装上限')
    cpxx = models.FloatField(blank=True, null=True, verbose_name='包装下限')
    zbq = models.IntegerField(blank=True, null=True, verbose_name='保质期')  # 表单后面添加天字
    cctj = models.CharField(max_length=50, blank=True, null=True, verbose_name='储存条件')
    cpsb = models.CharField(max_length=50, blank=True, null=True, verbose_name='产品商标')
    cppic = models.ImageField(upload_to=user_directory_path, verbose_name='产品图片', null=True, blank=True)
    cpsm = models.FileField(upload_to=user_directory_path, verbose_name='产品说明', null=True, blank=True)
    tempname = models.FileField(upload_to=user_directory_path, verbose_name='成品标签模板', null=True, blank=True)  # (下完计划后，打印标签模板名称)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.cpid

    class Meta:
        db_table = 'cpml'
        verbose_name = '产品'
        verbose_name_plural = '产品目录基础表'

































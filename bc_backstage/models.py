from django.db import models


class KhFk(models.Model):
    kh_name = models.CharField(max_length=20, verbose_name='姓名')
    kh_phone = models.IntegerField(verbose_name='联系方式')
    kh_mailbox = models.CharField(max_length=20, verbose_name='电子邮箱', blank=True)
    tj_date = models.DateField(auto_now_add=True, verbose_name='提交日期')
    fk_opinion = models.TextField(verbose_name='产品反馈意见')
    ip_address = models.GenericIPAddressField(protocol='IPv4', unpack_ipv4=False, verbose_name='IP')
    scph = models.ForeignKey('bc_production.Scjhb', on_delete=models.CASCADE, verbose_name='生产批号')

    class Meta:
        db_table = 'khfk'
        verbose_name = '反馈意见'
        verbose_name_plural = '客户反馈意见'


class DataGl(models.Model):
    zsph = models.CharField(max_length=20, verbose_name='追溯批号')
    cp_bh = models.CharField(max_length=20, verbose_name='产品编号')
    cp_name = models.CharField(max_length=50, verbose_name='产品名字')
    cp_date = models.DateField(verbose_name='生产日期')
    zs_date = models.DateField(auto_now_add=True, verbose_name='追溯日期')
    ip_address = models.GenericIPAddressField(protocol='IPv4', verbose_name='IP')

    class Meta:
        db_table = 'datagl'
        verbose_name = '后台数据管理'
        verbose_name_plural = '后台数据管理'

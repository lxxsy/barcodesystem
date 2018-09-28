# Generated by Django 2.0.1 on 2018-09-20 14:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('bc_formula', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cpml',
            fields=[
                ('cpid', models.CharField(max_length=50, primary_key=True, serialize=False, verbose_name='产品编号')),
                ('cpmc', models.CharField(max_length=50, verbose_name='产品名称')),
                ('gg', models.CharField(blank=True, max_length=20, null=True, verbose_name='规格')),
                ('dbz', models.CharField(blank=True, max_length=20, verbose_name='单包重')),
                ('pw', models.CharField(blank=True, max_length=50, verbose_name='批准文号')),
                ('bz', models.CharField(blank=True, max_length=50, verbose_name='标准编号')),
                ('cpxkz', models.CharField(blank=True, max_length=50, verbose_name='产品许可证')),
                ('cpsx', models.IntegerField(blank=True, null=True, verbose_name=' 包装上限')),
                ('cpxx', models.IntegerField(blank=True, null=True, verbose_name='包装下限')),
                ('zbq', models.IntegerField(blank=True, null=True, verbose_name='保质期')),
                ('cctj', models.CharField(blank=True, max_length=50, null=True, verbose_name='储存条件')),
                ('cpsb', models.CharField(blank=True, max_length=50, verbose_name='产品商标')),
                ('cppic', models.ImageField(upload_to='bc_products/cppic/%Y/%m/%d', verbose_name='产品图片')),
                ('cpsm', models.FileField(upload_to='bc_products/cpsm/%Y/%m/%d', verbose_name='产品说明')),
                ('tempname', models.FileField(upload_to='bc_products/cptemp/%Y/%m/%d', verbose_name='成品标签模板')),
                ('pbbh', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bc_formula.Pb', verbose_name='配方编号')),
            ],
            options={
                'verbose_name': '产品',
                'verbose_name_plural': '产品目录基础表',
                'db_table': 'cpml',
            },
        ),
        migrations.CreateModel(
            name='Cprk',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cpph', models.CharField(max_length=50, verbose_name='成品批号')),
                ('cpid', models.CharField(max_length=20, verbose_name='成品编号')),
                ('cpmc', models.CharField(max_length=20, verbose_name='成品名称')),
                ('rkdate', models.DateTimeField(auto_now_add=True, verbose_name='入库日期')),
                ('rksl', models.IntegerField(verbose_name='入库数量')),
                ('bz', models.CharField(blank=True, max_length=50, null=True, verbose_name='备注')),
                ('rkczy', models.CharField(blank=True, max_length=50, null=True, verbose_name='入库操作员')),
                ('rklxid', models.IntegerField(blank=True, null=True, verbose_name='入库类型ID')),
            ],
            options={
                'verbose_name': '成品',
                'verbose_name_plural': '成品入库表',
                'db_table': 'cprk',
            },
        ),
    ]

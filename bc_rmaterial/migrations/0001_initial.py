# Generated by Django 2.0.1 on 2018-08-27 15:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Stockinfo',
            fields=[
                ('stockid', models.CharField(max_length=20, primary_key=True, serialize=False, verbose_name='仓库编号')),
                ('stockname', models.CharField(blank=True, max_length=50, null=True, verbose_name='仓库名称')),
            ],
            options={
                'verbose_name': '仓库',
                'verbose_name_plural': '仓库基础表',
                'db_table': 'stockinfo',
            },
        ),
        migrations.CreateModel(
            name='Ylfl',
            fields=[
                ('flid', models.IntegerField(primary_key=True, serialize=False, verbose_name='分类编号')),
                ('fldm', models.CharField(blank=True, max_length=10, null=True, verbose_name='分类代码')),
                ('flmc', models.CharField(blank=True, max_length=50, null=True, verbose_name='名称')),
                ('flsm', models.CharField(blank=True, max_length=200, null=True, verbose_name='说明')),
            ],
            options={
                'verbose_name': '原料分类',
                'verbose_name_plural': '原料分类基础表',
                'db_table': 'ylfl',
            },
        ),
        migrations.CreateModel(
            name='Ylinfo',
            fields=[
                ('ylid', models.CharField(max_length=50, primary_key=True, serialize=False, verbose_name='原料代码')),
                ('ylname', models.CharField(max_length=50, verbose_name='名称')),
                ('dw', models.CharField(choices=[('0', 'kg'), ('1', 'g')], default='0', max_length=50, verbose_name='计量单位')),
                ('piedw', models.IntegerField(verbose_name='单包重量(kg)')),
                ('zczbq', models.IntegerField(default=365, verbose_name='最长质保期(天)')),
                ('zjzbq', models.IntegerField(default=365, verbose_name='最佳质保期(天)')),
                ('park', models.IntegerField(blank=True, null=True, verbose_name='存放仓位(1~60)用于原料指定料桶')),
                ('bz', models.CharField(blank=True, max_length=100, null=True, verbose_name='备注')),
                ('pieprice', models.DecimalField(blank=True, decimal_places=2, max_digits=18, null=True, verbose_name='单价')),
                ('minsl', models.FloatField(verbose_name='最小库存')),
                ('maxsl', models.FloatField(verbose_name='最大库存')),
                ('tymc', models.CharField(blank=True, max_length=30, null=True, verbose_name='通用名称')),
                ('ysbz', models.IntegerField(blank=True, null=True, verbose_name='验收标准号')),
                ('ylzt', models.BooleanField(default=True, verbose_name='原料状态')),
                ('barcode', models.CharField(blank=True, max_length=50, null=True, verbose_name='原料条形码')),
                ('stockid', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='bc_rmaterial.Stockinfo', verbose_name='默认仓库')),
                ('zf', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='bc_rmaterial.Ylfl', verbose_name='原料分类')),
            ],
            options={
                'verbose_name': '原料',
                'verbose_name_plural': '原料基础信息表',
                'db_table': 'ylinfo',
            },
        ),
    ]

# Generated by Django 2.0.1 on 2018-09-05 10:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('bc_production', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Qjybg',
            fields=[
                ('bgbh', models.CharField(max_length=20, primary_key=True, serialize=False, verbose_name='报告编号')),
                ('cpmc', models.CharField(max_length=50, verbose_name='产品名称')),
                ('scrq', models.DateField(verbose_name='生产日期')),
                ('gg', models.CharField(blank=True, max_length=50, verbose_name='规格')),
                ('pzr', models.CharField(blank=True, max_length=20, null=True, verbose_name='批准人')),
                ('bz', models.CharField(blank=True, max_length=500, null=True, verbose_name='备注')),
                ('jybgfile', models.FileField(null=True, upload_to='bc_test/jybg/%Y/%m/%d', verbose_name='检验报告文件')),
                ('qypqy', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='bc_production.Scjhb', verbose_name='检验批号')),
            ],
            options={
                'verbose_name': '检验报告',
                'verbose_name_plural': '检验报告',
                'db_table': 'qjybg',
            },
        ),
    ]

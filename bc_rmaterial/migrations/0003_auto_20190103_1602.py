# Generated by Django 2.0.1 on 2019-01-03 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bc_rmaterial', '0002_enterstock_stock'),
    ]

    operations = [
        migrations.CreateModel(
            name='SystemParameter',
            fields=[
                ('id', models.CharField(max_length=10, primary_key=True, serialize=False, verbose_name='寻找数据的唯一标识')),
                ('lldh', models.IntegerField(verbose_name='领料单号生成')),
                ('scph', models.IntegerField(default=None, verbose_name='生产批号生成')),
            ],
            options={
                'verbose_name': '系统参数',
                'verbose_name_plural': '系统参数',
                'db_table': 'system_parameter',
            },
        ),
        migrations.AlterModelOptions(
            name='enterstock',
            options={'verbose_name': '原料入库', 'verbose_name_plural': '原料入库信息'},
        ),
        migrations.AlterModelOptions(
            name='gys',
            options={'verbose_name': '供应商', 'verbose_name_plural': '供应商信息'},
        ),
        migrations.AlterModelOptions(
            name='stockinfo',
            options={'verbose_name': '仓库', 'verbose_name_plural': '仓库信息'},
        ),
        migrations.AlterModelOptions(
            name='ylfl',
            options={'verbose_name': '原料分类', 'verbose_name_plural': '原料分类'},
        ),
        migrations.AlterModelOptions(
            name='ylinfo',
            options={'verbose_name': '原料', 'verbose_name_plural': '原料基础信息'},
        ),
    ]
# Generated by Django 2.0.1 on 2018-07-02 12:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bc_product', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Enterstockcp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lot', models.CharField(max_length=50, verbose_name='批号')),
                ('rdate', models.DateTimeField(auto_now_add=True, verbose_name='入库日期')),
                ('rsl', models.FloatField(verbose_name='入库数量')),
                ('bz', models.CharField(blank=True, max_length=50, null=True, verbose_name='备注')),
                ('actionid', models.CharField(blank=True, max_length=50, null=True, verbose_name='入库操作员账号')),
                ('bar', models.CharField(blank=True, max_length=50, null=True, verbose_name='成品条码')),
                ('rklxid', models.IntegerField(blank=True, null=True, verbose_name='入库类型ID')),
            ],
            options={
                'verbose_name': '成品',
                'verbose_name_plural': '成品入库表',
                'db_table': 'EnterStockCP',
            },
        ),
        migrations.AlterField(
            model_name='cpml',
            name='cpsb',
            field=models.CharField(blank=True, max_length=50, verbose_name='产品商标'),
        ),
        migrations.AlterField(
            model_name='cpml',
            name='cptp',
            field=models.ImageField(blank=True, upload_to='bc_products', verbose_name='产品图片'),
        ),
        migrations.AddField(
            model_name='enterstockcp',
            name='cpid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bc_product.Cpml', verbose_name='产品代码'),
        ),
    ]
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
            name='DataGl',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('zsph', models.CharField(max_length=20, verbose_name='追溯批号')),
                ('cp_bh', models.CharField(max_length=20, verbose_name='产品编号')),
                ('cp_name', models.CharField(max_length=50, verbose_name='产品名字')),
                ('cp_date', models.DateField(verbose_name='生产日期')),
                ('zs_date', models.DateField(auto_now_add=True, verbose_name='追溯日期')),
                ('ip_address', models.GenericIPAddressField(protocol='IPv4', verbose_name='IP')),
            ],
            options={
                'verbose_name': '后台数据管理',
                'verbose_name_plural': '后台数据管理',
                'db_table': 'datagl',
            },
        ),
        migrations.CreateModel(
            name='KhFk',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kh_name', models.CharField(max_length=20, verbose_name='姓名')),
                ('kh_phone', models.IntegerField(verbose_name='联系方式')),
                ('kh_mailbox', models.CharField(blank=True, max_length=20, verbose_name='电子邮箱')),
                ('tj_date', models.DateField(auto_now_add=True, verbose_name='提交日期')),
                ('fk_opinion', models.TextField(verbose_name='产品反馈意见')),
                ('ip_address', models.GenericIPAddressField(protocol='IPv4', verbose_name='IP')),
                ('scph', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bc_production.Scjhb', verbose_name='生产批号')),
            ],
            options={
                'verbose_name': '反馈意见',
                'verbose_name_plural': '客户反馈意见',
                'db_table': 'khfk',
            },
        ),
    ]

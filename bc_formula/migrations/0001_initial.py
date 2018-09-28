# Generated by Django 2.0.1 on 2018-09-20 14:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('bc_rmaterial', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pb',
            fields=[
                ('pbbh', models.CharField(max_length=50, primary_key=True, serialize=False, verbose_name='配方编号')),
                ('pbname', models.CharField(max_length=50, verbose_name='配方名称')),
                ('pftype', models.CharField(choices=[('ONE', '标准配方'), ('TWO', '比例配方')], default='ONE', max_length=15, verbose_name='配方类型')),
                ('scsx', models.IntegerField(blank=True, null=True, verbose_name='生产顺序')),
                ('scxh', models.IntegerField(blank=True, default=1, null=True, verbose_name='默认生产线')),
                ('yx', models.BooleanField(default=True, verbose_name='有效配方')),
                ('bz', models.CharField(blank=True, max_length=220, null=True, verbose_name='备注')),
            ],
            options={
                'verbose_name': '配方',
                'verbose_name_plural': '配方',
                'db_table': 'pb',
            },
        ),
        migrations.CreateModel(
            name='Pbf',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plno', models.IntegerField(verbose_name='序号')),
                ('bzgl', models.FloatField(verbose_name='标准值')),
                ('topz', models.FloatField(verbose_name='上限')),
                ('lowz', models.FloatField(verbose_name='下限')),
                ('dw', models.CharField(choices=[('ONE', 'kg'), ('TWO', 'g')], default='ONE', max_length=20, verbose_name='单位')),
                ('jno', models.IntegerField(verbose_name='投料顺序')),
                ('lt', models.BooleanField(default=True, verbose_name='称零头')),
                ('zs', models.BooleanField(default=True, verbose_name='追溯')),
                ('pbbh', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bc_formula.Pb', verbose_name='配方编号')),
                ('ylid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bc_rmaterial.Ylinfo', verbose_name='原料代码')),
            ],
            options={
                'verbose_name': '配方副表',
                'verbose_name_plural': '配方副表',
                'db_table': 'pbf',
            },
        ),
    ]

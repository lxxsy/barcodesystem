# Generated by Django 2.0.1 on 2018-07-05 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bc_production', '0003_auto_20180705_0934'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scjhb',
            name='rq',
            field=models.DateField(verbose_name='日期'),
        ),
    ]

# Generated by Django 2.0.1 on 2019-02-21 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bc_formula', '0002_auto_20190103_1055'),
    ]

    operations = [
        migrations.AddField(
            model_name='pb',
            name='validity',
            field=models.BooleanField(default=False, verbose_name='有无产品'),
        ),
    ]

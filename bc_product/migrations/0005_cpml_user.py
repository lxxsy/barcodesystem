# Generated by Django 2.0.1 on 2019-02-25 09:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bc_product', '0004_auto_20190221_1616'),
    ]

    operations = [
        migrations.AddField(
            model_name='cpml',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]

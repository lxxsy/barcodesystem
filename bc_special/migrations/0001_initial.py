# Generated by Django 2.0.1 on 2019-06-13 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Special',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('batch_num', models.CharField(max_length=20)),
                ('batch_url', models.CharField(max_length=100)),
            ],
        ),
    ]
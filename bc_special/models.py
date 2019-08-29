from django.db import models


class Special(models.Model):
    batch_num = models.CharField(max_length=20)
    batch_url = models.CharField(max_length=100)

    class Meta:
        db_table = 'special'

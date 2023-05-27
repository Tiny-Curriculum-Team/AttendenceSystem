from django.db import models


# Create your models here.
class Number(models.Model):
    date_time=models.TimeField()
    count=models.IntegerField()

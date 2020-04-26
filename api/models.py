from django.db import models


# Create your models here.
class UserData(models.Model):
    name = models.CharField(max_length=30)
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    long = models.DecimalField(max_digits=9, decimal_places=6)
    image = models.FileField()
    age = models.IntegerField(max_length=2)


class Disease(models.Model):
    name = models.CharField(max_length=250)
    point = models.IntegerField()
    level = models.IntegerField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    # 6254601

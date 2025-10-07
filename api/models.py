from django.db import models

# Create your models here.
class Solar(models.Model):
    solarId = models.AutoField(primary_key=True, auto_created=True)
    load = models.IntegerField()
    gridStatus = models.BooleanField(default = False)
    solarValue = models.IntegerField(default=0)


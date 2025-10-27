from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Solar(models.Model):
    solarId = models.AutoField(primary_key=True, auto_created=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    load = models.IntegerField(default=0)
    gridStatus = models.BooleanField(default = False)
    solarValue = models.IntegerField(default=0)
    isBateryFull = models.BooleanField(default= False)
    batteryValue = models.IntegerField(default=0)
    invertorCapacity = models.IntegerField(default=0)
    instaledSolarPower = models.IntegerField(default=0)
    batteryCapacity = models.IntegerField(default=0)

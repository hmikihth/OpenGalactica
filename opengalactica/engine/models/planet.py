from django.db import models
from django.conf import settings

class Planet(models.Model):
    name = models.CharField(max_length=128)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    x = models.IntegerField(default=0)
    y = models.IntegerField(default=0)
    z = models.IntegerField(default=0)
    w = models.IntegerField(default=0)
    tp = models.IntegerField(default=0)
    point = models.IntegerField(default=0)
    metal = models.IntegerField(default=0)
    crystal = models.IntegerField(default=0)
    narion = models.IntegerField(default=0)
    credit = models.IntegerField(default=0)
    alliance = models.ForeignKey("Alliance", on_delete=models.SET_NULL, null=True)
    protection = models.IntegerField(default=72)

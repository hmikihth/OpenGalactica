from django.db import models

class Player(models.Model):
    name = models.CharField(max_length=128)
    x = models.IntegerField(default=0)
    y = models.IntegerField(default=0)
    z = models.IntegerField(default=0)
    w = models.IntegerField(default=0)
    tp = models.IntegerField(default=0)
    point = models.IntegerField(default=0)
    alliance = models.ForeignKey("Alliance", on_delete=models.SET_NULL, null=True)
    protection = models.IntegerField(default=72)

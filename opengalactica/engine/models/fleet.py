from django.db import models

class Fleet(models.Model):
    name = models.CharField(max_length=128)
    base = models.BooleanField(default=False)
    owner = models.ForeignKey("Player", on_delete=models.CASCADE, related_name="owner")
    formation = models.CharField(max_length=8, default="wall")
    target = models.ForeignKey("Player", on_delete=models.SET_NULL, related_name="target", null=True)
    distance = models.IntegerField(null=True)
    task = models.CharField(max_length=8, null=True)
    
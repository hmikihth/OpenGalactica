from django.db import models

class Alliance(models.Model):
    name = models.CharField(max_length=128)
    identifier = models.CharField(max_length=6)

from django.db import models

class AllianceRank(models.Model):
    name = models.CharField(max_length=64)
    alliance_type = models.CharField(max_length=64, default="standard")
    is_founder = models.BooleanField(default=False)
    can_invite_members = models.BooleanField(default=False)
    can_remove_members = models.BooleanField(default=False)
    can_distribute_resources = models.BooleanField(default=False)
    can_manage_forum = models.BooleanField(default=False)
    can_set_tax = models.BooleanField(default=False)
    can_set_ranks = models.BooleanField(default=False)
    can_set_attack = models.BooleanField(default=False)
    can_set_defense = models.BooleanField(default=False)
    can_set_diplomacy = models.BooleanField(default=False)
    can_set_research = models.BooleanField(default=False)
    can_set_voting = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name

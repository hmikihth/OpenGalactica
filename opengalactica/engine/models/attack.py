from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
#from engine.models import Planet, Alliance

class Attack(models.Model):
    organizer = models.ForeignKey("engine.Planet", on_delete=models.CASCADE)
    alliance = models.ForeignKey("engine.Alliance", on_delete=models.CASCADE)
    short_description = models.CharField(max_length=255)
    description = models.TextField()
    start = models.IntegerField()

    def __str__(self):
        return f"{self.short_description} (Start: {self.start})"


class AttackTarget(models.Model):
    attack = models.ForeignKey(Attack, on_delete=models.CASCADE)
    target = models.ForeignKey("engine.Planet", on_delete=models.CASCADE)
    description = models.TextField()

    def __str__(self):
        return f"Target: {self.target} for Attack: {self.attack.short_description}"


class AttackSubscription(models.Model):
    attack_target = models.ForeignKey(AttackTarget, on_delete=models.CASCADE)
    subscriber = models.ForeignKey("engine.Planet", on_delete=models.CASCADE)
    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.subscriber} subscribed to {self.attack_target}"


@receiver(pre_save, sender="engine.Planet")
def delete_attack_subscriptions_on_leave(sender, instance, **kwargs):
    if instance.pk:
        try:
            original = sender.objects.get(pk=instance.pk)
            if original.alliance and instance.alliance is None:
                AttackSubscription.objects.filter(subscriber=instance).delete()
        except sender.DoesNotExist:
            pass
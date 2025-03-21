from django.db import models

class Defense(models.Model):
    organizer = models.ForeignKey("engine.Planet", on_delete=models.CASCADE)
    alliance = models.ForeignKey("engine.Alliance", on_delete=models.CASCADE)
    short_description = models.CharField(max_length=255)
    description = models.TextField()
    arrival = models.IntegerField()

    def __str__(self):
        return f"{self.short_description} (Arrival: {self.arrival})"
        
    def add_target(self, target, description):
        DefenseTarget.objects.create(defense=self, target=target, description=description)


class DefenseTarget(models.Model):
    defense = models.ForeignKey(Defense, on_delete=models.CASCADE)
    target = models.ForeignKey("engine.Planet", on_delete=models.CASCADE)
    description = models.TextField()

    def __str__(self):
        return f"Target: {self.target} for Defense: {self.defense.short_description}"

from django.db import models

class Diplomacy(models.Model):
    DIPLOMACY_TYPES = [
        ("Neutral", "Neutral"),
        ("Ally", "Ally"),
        ("War", "War"),
        ("Trade", "Trade"),
        ("Non-Aggression Pact", "Non-Aggression Pact"),
    ]

    sender = models.ForeignKey("Alliance", on_delete=models.CASCADE, related_name="sent_diplomacies")
    receiver = models.ForeignKey("Alliance", on_delete=models.CASCADE, related_name="received_diplomacies")
    diplo_type = models.CharField(max_length=50, choices=DIPLOMACY_TYPES)
    expiration = models.IntegerField()  # The turn when it will expire
    termination = models.IntegerField()  # Turns necessary until it becomes outdated if broken
    description = models.TextField(blank=True, null=True)
    accepted = models.BooleanField(default=False)  # Becomes True when the receiver accepts the diplomacy

    class Meta:
        unique_together = ("sender", "receiver", "diplo_type")

    def __str__(self):
        return f"{self.sender} - {self.receiver}: {self.diplo_type} (Exp: {self.expiration}, Accepted: {self.accepted})"
    
    def accept(self):
        """Method for the receiver to accept the diplomacy."""
        self.accepted = True
        self.save()

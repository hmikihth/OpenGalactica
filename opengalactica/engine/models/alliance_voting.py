from django.db import models
from django.core.exceptions import ValidationError

class AllianceVoting(models.Model):
    alliance = models.ForeignKey("Alliance", on_delete=models.CASCADE, related_name="votings")
    title = models.CharField(max_length=255)
    description = models.TextField()
    public = models.BooleanField(default=False)
    end = models.IntegerField()  # The turn when voting ends

    def __str__(self):
        return f"{self.title} ({self.alliance.name})"


class AllianceVotingChoice(models.Model):
    voting = models.ForeignKey(AllianceVoting, on_delete=models.CASCADE, related_name="choices")
    label = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.label} (Voting: {self.voting.title})"


class AllianceVote(models.Model):
    voting = models.ForeignKey(AllianceVoting, on_delete=models.CASCADE, related_name="votes")
    member = models.ForeignKey("Planet", on_delete=models.CASCADE, related_name="votes")
    choice = models.ForeignKey(AllianceVotingChoice, on_delete=models.CASCADE, related_name="votes")
    note = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ("voting", "member")  # Ensures a member can vote only once per voting

    def save(self, *args, **kwargs):
        from engine.models import Round
        round = Round.objects.filter(active=True).order_by("number").last()
        current_turn = round.turn
        if self.voting.end < current_turn:
            raise ValidationError("Voting has ended.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.member.name} voted for {self.choice.label} in {self.voting.title}"

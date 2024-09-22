from django.db import models

from .round import Round

class AllianceInvitation(models.Model):
    planet = models.ForeignKey("Planet", on_delete=models.CASCADE)
    alliance = models.ForeignKey("Alliance", on_delete=models.CASCADE)
    invited_by = models.ForeignKey("Planet", on_delete=models.SET_NULL, null=True, related_name="sent_invitations")
    sent_turn = models.IntegerField()
    accepted = models.BooleanField(default=False)
    accepted_turn = models.IntegerField(null=True, blank=True)
    rejected = models.BooleanField(default=False)
    rejected_turn = models.IntegerField(null=True, blank=True)
    message = models.TextField(null=True, blank=True)

    def accept(self):
        if self.accepted:
            raise ValueError("This invitation is already accepted!")
        if self.rejected:
            raise ValueError("This invitation is already rejected!")
        current_turn = Round.objects.all().order_by("number").last().turn
        self.planet.alliance = self.alliance
        self.planet.save()
        self.accepted = True
        self.accepted_turn = current_turn
        self.save()

        self.planet.alliance = self.alliance
        self.planet.rank = None
        self.planet.save()


    def reject(self):
        if self.accepted:
            raise ValueError("This invitation is already accepted!")
        if self.rejected:
            raise ValueError("This invitation is already rejected!")
        current_turn = Round.objects.all().order_by("number").last().turn
        self.rejected = True
        self.rejected_turn = current_turn
        self.save()

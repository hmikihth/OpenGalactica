from django.db import models
from django.utils import timezone
    
class Message(models.Model):
    sender = models.ForeignKey("Planet", related_name="sender", on_delete=models.SET_NULL, null=True)
    receiver = models.ForeignKey("Planet", related_name="receiver", on_delete=models.SET_NULL, null=True)
    round = models.IntegerField()  # Game round when the message was created
    turn = models.IntegerField()   # Game turn when the message was created
    server_time = models.DateTimeField(default=timezone.now)  # Automatically set to current server time
    title = models.CharField(max_length=255)  # Title of the message
    content = models.TextField()
    alliance = models.ForeignKey("Alliance", on_delete=models.SET_NULL, null=True, blank=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return self.title

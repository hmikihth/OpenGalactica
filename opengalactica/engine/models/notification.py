from django.db import models
from django.utils import timezone
    
class Notification(models.Model):
    planet = models.ForeignKey("Planet", on_delete=models.CASCADE)  # Link to the Planet model
    round = models.IntegerField()  # Game round when the notification was created
    turn = models.IntegerField()   # Game turn when the notification was created
    server_time = models.DateTimeField(default=timezone.now)  # Automatically set to current server time
    ntype = models.CharField(max_length=255) # Notification type for filtering. Examples: "War", "Research", "Building", "Production", "News", etc... 
    content = models.JSONField()  # JSON content
    read = models.BooleanField(default=False)

    def __str__(self):
        return self.content

from django.db import models

class Round(models.Model):
    number = models.IntegerField(default=1)
    turn = models.IntegerField(default=1)
    
    def tick(self):
        self.turn += 1
        self.save()
        return self.turn
        
    def new_round(self):
        self.number += 1
        self.turn = 1
        self.save()

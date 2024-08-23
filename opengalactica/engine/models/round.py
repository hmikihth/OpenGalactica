from django.db import models

class Round(models.Model):
    number = models.IntegerField(default=1)
    turn = models.IntegerField(default=1)
    active = models.BooleanField(default=True)
    calculate = models.BooleanField(default=False)
    
    def start_calculations(self):
        self.calculate = True
        self.save()
    
    def end_calculations(self):
        self.calculate = False
        self.save()

    def tick(self):
        self.turn += 1
        self.save()
        return self.turn
        
    def new_round(self):
        self.number += 1
        self.turn = 1
        self.save()

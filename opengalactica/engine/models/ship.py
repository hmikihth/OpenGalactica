from django.db import models

class ShipClass(models.Model):
    name = models.CharField(max_length=128)
    identifier = models.CharField(max_length=6)


class ShipModel(models.Model):
    name = models.CharField(max_length=128)
    ship_class =  models.ForeignKey("ShipClass", on_delete=models.SET_NULL, null=True)
    

class ShipProto():
    loss = 0
    blocked = 0
    stolen = 0
    new_loss = 0
    new_blocked = 0
    new_stolen = 0
    remaining = 0
    combat_ready = 0

    def set_quantity(self, quantity):
        self.quantity = quantity
        self.remaining = quantity
        self.combat_ready = quantity

class Ship(ShipClass, ShipProto):
    ship_model = models.ForeignKey("ShipModel", on_delete=models.CASCADE)
    fleet =  models.ForeignKey("Fleet", on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    
    
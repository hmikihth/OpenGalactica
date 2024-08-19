from rest_framework import serializers

from engine.models import ShipModel

class ShipModelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ShipModel
        fields = [
            "name",
            "pds", 
            "species",
            "ship_class",
            "target1",
            "target2",
            "target3",
            "weapon_type",
            "initiative",
            "evasion",
            "weapon_count",
            "accuracy_points",
            "damage",
            "hp",
            "metal",
            "crystal",
            "narion",
            "fuel",
            "production_time",
            "travel_g",
            "travel_s",
            "travel_u"
        ]

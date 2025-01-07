from rest_framework import serializers
from engine.models import (
    Species, ShipModel, Alliance, Sol, Planet, News, Encyclopedia,
    StockedSatellite, Ship, Fleet, PlanetResearch, Message
)

# Public Serializers
class TimeSerializer(serializers.Serializer):
    round = serializers.IntegerField()
    turn = serializers.IntegerField()
    minutes = serializers.IntegerField()
    seconds = serializers.IntegerField()

class SpeciesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Species
        fields = '__all__'

class ShipModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShipModel
        fields = '__all__'

class AllianceToplistSerializer(serializers.Serializer):
    rank = serializers.IntegerField()
    name = serializers.CharField()
    points = serializers.IntegerField()

class SolToplistSerializer(serializers.Serializer):
    rank = serializers.IntegerField()
    name = serializers.CharField()
    points = serializers.IntegerField()

class PlanetToplistSerializer(serializers.Serializer):
    rank = serializers.IntegerField()
    name = serializers.CharField()
    alliance = serializers.CharField()
    points = serializers.IntegerField()


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['id', 'author', 'round', 'turn', 'server_time', 'title', 'content', 'slug']
        read_only_fields = ['id', 'author', 'round', 'turn', 'server_time', 'slug']  # author and slug will be set automatically

    def create(self, validated_data):
        # Slug generation will be handled in the News model's save method
        return super().create(validated_data)


class EncyclopediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Encyclopedia
        fields = ['title', 'content', 'slug']
        read_only_fields = ['slug']

# Private Serializers
class PlanetDataSerializer(serializers.ModelSerializer):
    point_diff = serializers.SerializerMethodField()
    xp_diff = serializers.SerializerMethodField()
    coordinates = serializers.SerializerMethodField()

    class Meta:
        model = Planet
        fields = '__all__'

    def get_point_diff(self, obj):
        return (obj.points or 0) - (obj.points_before or 0)

    def get_xp_diff(self, obj):
        return (obj.xp or 0) - (obj.xp_before or 0)
        
    def get_coordinates(self, obj):
        return obj.coordinates


class PDSSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    quantity = serializers.IntegerField()

class AvailablePDSSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    active = serializers.BooleanField()

class SatelliteSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    quantity = serializers.IntegerField()

class AvailableSatelliteSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    active = serializers.BooleanField()

class ShipSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    ship_class = serializers.CharField()
    quantity = serializers.IntegerField()

class AvailableShipSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    active = serializers.BooleanField()


class FleetSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    target = serializers.SerializerMethodField()
    task = serializers.SerializerMethodField()

    class Meta:
        model = Fleet
        fields = ['name', 'active', 'task', 'status', 'distance', 'turns', 'target']
        
    def get_task(self, obj):
        if obj.role == "Attackers" and obj.task == "move":
            return f"Attack ({obj.turns} turns)" 
        elif obj.role == "Defenders" and obj.task == "move":
            return f"Defend ({obj.turns} turns)"
        else: 
            return "-"
        
    def get_target(self, obj):
        return str(obj.target)

    def get_status(self, obj):
        if obj.task == "move":
            if obj.distance == 0:
                return f"Fighting ({obj.turns} turns)"
            return f"On the way ({obj.distance} turns)"
        elif obj.task == "return":
            return f"Returning ({obj.distance} turns)"
        return "On base"


class ResearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanetResearch
        fields = "__all__"
        
# Serializer for listing received/sent messages (excluding content)
class MessageListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        exclude = ['content']

# Serializer for reading a message (full data)
class MessageDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'

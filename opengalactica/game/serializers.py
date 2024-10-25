from rest_framework import serializers
from engine.models import (
    Species, ShipModel, Alliance, Sol, Planet, News, Encyclopedia,
    StockedSatellite, Ship, Fleet, PlanetResearch
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
    class Meta:
        model = Fleet
        fields = ['name', 'active', 'status', 'distance', 'turns']

    def get_status(self, obj):
        status = "Base"
        if obj.task == "move":
            status = obj.role[:-3]
        elif obj.task == "return":
            status = obj.task
        return status


class ResearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanetResearch
        fields = "__all__"

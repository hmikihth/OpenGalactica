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


class IncomingSerializer(serializers.ModelSerializer):
    target = serializers.SerializerMethodField()
    owner = serializers.SerializerMethodField()
    species = serializers.SerializerMethodField()
    alliance = serializers.SerializerMethodField()
    points = serializers.SerializerMethodField()
    ships = serializers.SerializerMethodField()
    arrival = serializers.SerializerMethodField()

    class Meta:
        model = Fleet
        fields = ['role', 'species', 'owner', 'alliance', 'points', 'ships', 'distance', 'arrival', 'target']

    def get_target(self, obj):
        return str(obj.target)
        
    def get_owner(self, obj):
        return str(obj.owner)
        
    def get_species(self, obj):
        return obj.owner.species
        
    def get_alliance(self, obj):
        return f"#{obj.owner.alliance.identifier}"
        
    def get_points(self, obj):
        return obj.owner.points
        
    def get_ships(self, obj):
        return obj.n_ships
        
    def get_arrival(self, obj):
        from engine.models import Round
        round = Round.objects.filter(active=True).order_by("number").last()
        return  round.turn + obj.distance
        
        
class OutgoingSerializer(serializers.ModelSerializer):
    target = serializers.SerializerMethodField()
    owner = serializers.SerializerMethodField()
    species = serializers.SerializerMethodField()
    alliance = serializers.SerializerMethodField()
    points = serializers.SerializerMethodField()
    ships = serializers.SerializerMethodField()
    arrival = serializers.SerializerMethodField()

    class Meta:
        model = Fleet
        fields = ['role', 'owner', 'ships', 'distance', 'arrival', 'species', 'target', 'alliance', 'points']

    def get_target(self, obj):
        return str(obj.target)
        
    def get_owner(self, obj):
        return str(obj.owner)
        
    def get_species(self, obj):
        return obj.target.species
        
    def get_alliance(self, obj):
        return f"#{obj.target.alliance.identifier}"
        
    def get_points(self, obj):
        return obj.target.points
        
    def get_ships(self, obj):
        return obj.n_ships
        
    def get_arrival(self, obj):
        from engine.models import Round
        round = Round.objects.filter(active=True).order_by("number").last()
        return  round.turn + obj.distance
        

class ResearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanetResearch
        fields = "__all__"
        
# Serializer for listing received/sent messages (excluding content)
class MessageListSerializer(serializers.ModelSerializer):
    sender = serializers.SerializerMethodField()
    receiver = serializers.SerializerMethodField()
    
    class Meta:
        model = Message
        exclude = ['content']

    def get_sender(self, obj):
        return str(obj.sender)

    def get_receiver(self, obj):
        return str(obj.receiver)


# Serializer for reading a message (full data)
class MessageDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'


class CommunicationSerializer(serializers.Serializer):
    new_events = serializers.IntegerField()
    new_messages = serializers.IntegerField()
    

class MinistersMessageSerializer(serializers.ModelSerializer):
    ministers_message = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = Sol
        fields = ["id", "ministers_message"]

class AllianceNewsSerializer(serializers.ModelSerializer):
    news = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = Alliance
        fields = ["id", "news"]

class LatestNewsSerializer(serializers.ModelSerializer):
    timestamp = serializers.CharField(required=False, allow_blank=True)
    description = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = News
        fields = ["id", "slug","title","timestamp","description"]

class HomeTechnologySerializer(serializers.Serializer):
    research = serializers.CharField(required=False, allow_blank=True)
    research_turns = serializers.IntegerField()
    building = serializers.CharField(required=False, allow_blank=True)
    building_turns = serializers.IntegerField()

class PlasmatorSerializer(serializers.ModelSerializer):
    total_plasmators = serializers.SerializerMethodField()

    class Meta:
        model = Planet
        fields = ["metal_plasmator", "crystal_plasmator", "narion_plasmator", "neutral_plasmator", "total_plasmators"]
        
    def get_total_plasmators(self, obj):
        return obj.metal_plasmator + obj.crystal_plasmator + obj.narion_plasmator + obj.neutral_plasmator

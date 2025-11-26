from rest_framework import serializers
from engine.models import (
    Species, ShipModel, Alliance, Sol, Planet, News, Encyclopedia,
    SatelliteType, Ship, Fleet, PlanetResearch, Message
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
    species = serializers.CharField()
    name = serializers.CharField()
    alliance = serializers.CharField()
    points = serializers.IntegerField()


class XpToplistSerializer(serializers.Serializer):
    rank = serializers.IntegerField()
    species = serializers.CharField()
    name = serializers.CharField()
    xp = serializers.IntegerField()


class PlasmatorToplistSerializer(serializers.Serializer):
    rank = serializers.IntegerField()
    species = serializers.CharField()
    name = serializers.CharField()
    total_plasmators = serializers.IntegerField()


class SpeciesToplistSerializer(serializers.Serializer):
    rank = serializers.IntegerField()
    species = serializers.CharField()
    name = serializers.CharField()
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
    is_own = serializers.SerializerMethodField()
    sol = serializers.SerializerMethodField()
    alliance = serializers.SerializerMethodField()
    plasmators = serializers.SerializerMethodField()

    class Meta:
        model = Planet
        fields = '__all__'

    def get_point_diff(self, obj):
        return (obj.points or 0) - (obj.points_before or 0)

    def get_xp_diff(self, obj):
        return (obj.xp or 0) - (obj.xp_before or 0)
        
    def get_coordinates(self, obj):
        return obj.coordinates

    def get_is_own(self, obj):
        request = self.context.get('request', None)
        if request:
            return obj.user == request.user
        return False

    def get_sol(self, obj):
        return str(obj.sol)

    def get_alliance(self, obj):
        return str(obj.alliance)

    def get_plasmators(self, obj):
        return str(obj.plasmators)

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
        

class PlanetResearchSerializer(serializers.ModelSerializer):
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

class TechTreeSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    research_type = serializers.CharField()
    development_time = serializers.IntegerField()
    metal = serializers.IntegerField()
    crystal = serializers.IntegerField()
    narion = serializers.IntegerField()
    building = serializers.BooleanField()
    can_start = serializers.BooleanField()

    class Meta:
        model = PlanetResearch
        fields = "__all__"


class SingleResourceProductionSerializer(serializers.Serializer):
    amount = serializers.FloatField()
    plasmator_income = serializers.FloatField()
    planet_income = serializers.FloatField()
    minister = serializers.FloatField()
    tax = serializers.FloatField()
    net_income = serializers.FloatField()
    gross_income = serializers.FloatField()


class ResourceProductionSerializer(serializers.Serializer):
    metal = SingleResourceProductionSerializer()
    crystal = SingleResourceProductionSerializer()
    narion = SingleResourceProductionSerializer()
    neutral = SingleResourceProductionSerializer()
        
from engine.models import ShipModel

class ProductionShipModelSerializer(serializers.ModelSerializer):
    produced = serializers.SerializerMethodField()

    class Meta:
        model = ShipModel
        fields = [
            'id', 'name', 'ship_class',
            'target1', 'target2', 'target3',
            'metal', 'crystal', 'narion',
            'production_time', 'produced'
        ]

    def get_produced(self, obj):
        request = self.context.get('request', None)
        planet = Planet.objects.get(user=request.user)
        fleets = Fleet.objects.filter(owner=planet)
        qty = sum(map(lambda e:e.quantity, Ship.objects.filter(ship_model=obj, fleet__in=fleets)))
        return qty or 0

class ProduceSerializer(serializers.Serializer):
    ship_model = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)


from rest_framework import serializers

class ShipScrapSerializer(serializers.Serializer):
    ship_model = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)

class ShipOwnedSerializer(serializers.ModelSerializer):
    ship_model_name = serializers.CharField(source='ship_model.name')

    class Meta:
        model = Ship
        fields = ['id', 'ship_model', 'ship_model_name', 'quantity', 'metal', 'crystal', 'narion']

class SatelliteTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SatelliteType
        fields = [
            'id', 'name', 'code', 'description',
            'metal', 'crystal', 'narion',
            'production_time', 'requires_rocket', 'rocket_required_count'
        ]

class ProduceSatelliteSerializer(serializers.Serializer):
    satellite_type = serializers.PrimaryKeyRelatedField(queryset=SatelliteType.objects.all())
    quantity = serializers.IntegerField(min_value=1)

class FleetNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fleet
        fields = ['id', 'name']

class FleetFormationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fleet
        fields = ['id', 'name', 'formation']


class FleetControlSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fleet
        fields = [
            'id', 'name', 'task', 'status_display',
            'task_display', 'role', 'distance', 'turns',
            'target', 'base', 'x', 'y', 'z'
        ]

    status_display = serializers.SerializerMethodField()
    task_display = serializers.SerializerMethodField()
    x = serializers.SerializerMethodField()
    y = serializers.SerializerMethodField()
    z = serializers.SerializerMethodField()

    def get_status_display(self, obj):
        if obj.task == "move" and obj.role == "Attackers":
            return f"on the way to {obj.target} (distance: {obj.distance} turns)"
        elif obj.task == "move" and obj.role == "Defenders":
            return f"on the way to {obj.target} (distance: {obj.distance} turns)"
        elif obj.task == "return":
            return f"returning from {obj.target} (distance: {obj.distance} turns)"
        elif obj.task == "stand":
            return "on base"
        return "unknown"

    def get_task_display(self, obj):
        if obj.task == "move" and obj.role == "Attackers":
            return f"attack - {obj.turns} turns"
        elif obj.task == "move" and obj.role == "Attackers":
            return f"attack - {obj.turns} turns"
        return "-"
        
    def get_x(self, obj):
        if obj.target:
            return obj.target.x
        return None

    def get_y(self, obj):
        if obj.target:
            return obj.target.y
        return None

    def get_z(self, obj):
        if obj.target:
            return obj.target.z
        return None

class FleetsShipModelSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(required=True, allow_blank=False)
    ship_class = serializers.CharField(required=False, allow_blank=True)
    target1 = serializers.CharField(required=False, allow_blank=True)
    target2 = serializers.CharField(required=False, allow_blank=True)
    target3 = serializers.CharField(required=False, allow_blank=True)
    base = serializers.IntegerField()
    fleet1 = serializers.IntegerField()
    fleet2 = serializers.IntegerField()
    fleet3 = serializers.IntegerField()
    fleet4 = serializers.IntegerField()

    base_id = serializers.IntegerField()
    fleet1_id = serializers.IntegerField()
    fleet2_id = serializers.IntegerField()
    fleet3_id = serializers.IntegerField()
    fleet4_id = serializers.IntegerField()

    class Meta:
        fields = "__all__"

class FleetsFuelCostSerializer(serializers.Serializer):
    name = serializers.CharField(required=True, allow_blank=False)

    fleet1_fuel = serializers.IntegerField()
    fleet2_fuel = serializers.IntegerField()
    fleet3_fuel = serializers.IntegerField()
    fleet4_fuel = serializers.IntegerField()

    fleet1_distance = serializers.IntegerField()
    fleet2_distance = serializers.IntegerField()
    fleet3_distance = serializers.IntegerField()
    fleet4_distance = serializers.IntegerField()

class FcFleetListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fleet
        fields = ['id', 'name']

        
from engine.models import ProbeReport

class ProbeReportSerializer(serializers.ModelSerializer):
    alliance_identifier = serializers.SerializerMethodField()
    target_planet_name = serializers.SerializerMethodField()
    coordinates = serializers.SerializerMethodField()
    points = serializers.SerializerMethodField()

    class Meta:
        model = ProbeReport
        fields = '__all__'

    def get_alliance_identifier(self, obj):
        if obj.target_planet.alliance:
            return obj.target_planet.alliance.identifier

    def get_target_planet_name(self, obj):
        if obj.target_planet.name:
            return obj.target_planet.name

    def get_coordinates(self, obj):
        return obj.target_planet.coordinates

    def get_points(self, obj):
        return obj.target_planet.points
        
        
from engine.models import Notification
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'


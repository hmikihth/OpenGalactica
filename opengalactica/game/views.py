from django.utils.timezone import now

from django.db.models import Q

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAdminUser, SAFE_METHODS
from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework.parsers import MultiPartParser, FormParser

from engine.models import Species, ShipModel, Alliance, Sol, Planet, News, Encyclopedia
from engine.models import StockedSatellite, SatelliteType, Ship, Fleet, Round
from engine.models import PlanetResearch, SolResearch, AllianceResearch, Research
from engine.models import Message, Notification

from game.permissions import NewsAuthorOrReadOnly
from game.serializers import EncyclopediaSerializer


from game.serializers import (
    TimeSerializer, SpeciesSerializer, ShipModelSerializer, AllianceToplistSerializer, 
    SolToplistSerializer, PlanetToplistSerializer, XpToplistSerializer, PlasmatorToplistSerializer, 
    SpeciesToplistSerializer, NewsSerializer,# EncyclopediaSerializer,
    PlanetDataSerializer, PDSSerializer, AvailablePDSSerializer, SatelliteSerializer, AvailableSatelliteSerializer,
    ShipSerializer, AvailableShipSerializer, FleetSerializer, PlanetResearchSerializer, 
    MessageListSerializer, MessageDetailSerializer, CommunicationSerializer, IncomingSerializer, OutgoingSerializer,
    TechTreeSerializer, ResourceProductionSerializer, ProductionShipModelSerializer, FleetsShipModelSerializer,
    FcFleetListSerializer
)


# Public Viewsets
        
class TimeViewSet(ViewSet):
    permission_classes = [AllowAny]

    def list(self, request):
        rounds = Round.objects.all()
        if not rounds:
            round = Round.objects.create(number=1,turn=1)
        else:
            round = rounds.order_by("number").last()
        server_time = now()
        data = {
            "round": round.number,  # Replace with actual round number logic
            "turn": round.turn,  # Replace with actual turn number logic
            "minutes": server_time.minute,
            "seconds": server_time.second
        }
        serializer = TimeSerializer(data)
        return Response(serializer.data)


class SpeciesViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Species.objects.all()
    serializer_class = SpeciesSerializer


class ShipModelViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ShipModel.objects.filter(pds=False)
    serializer_class = ShipModelSerializer


class AllianceToplistViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def list(self, request):
        alliances = Alliance.objects.all()
        data = [{"name": a.name, "points": a.points} for a in alliances]
        data = sorted(data, key=lambda e:-e["points"])
        for i, e in enumerate(data):
            e["rank"] = i+1
        serializer = AllianceToplistSerializer(data, many=True)
        return Response(serializer.data)


class SolToplistViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def list(self, request):
        sols = Sol.objects.all()
        data = [{"name": f"{s.name} ({s.x}:{s.y})", "points": s.points} for s in sols]
        data = sorted(data, key=lambda e:-e["points"])
        for i, e in enumerate(data):
            e["rank"] = i+1
        serializer = SolToplistSerializer(data, many=True)
        return Response(serializer.data)


class PlanetToplistViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def list(self, request):
        planets = Planet.objects.all()
        data = [{"name": p.name, "alliance": str(p.alliance), "points": p.points, "species":p.species} for p in planets]
        data = sorted(data, key=lambda e:-e["points"])
        for i, e in enumerate(data):
            e["rank"] = i+1
        serializer = PlanetToplistSerializer(data, many=True)
        return Response(serializer.data)
        

class XpToplistViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def list(self, request):
        planets = Planet.objects.all()
        data = [{"name": p.name, "xp": p.xp, "species":p.species} for p in planets]
        data = sorted(data, key=lambda e: -e["xp"])[:10]

        for i, e in enumerate(data):
            e["rank"] = i + 1

        serializer = XpToplistSerializer(data, many=True)
        return Response(serializer.data)


class PlasmatorToplistViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def list(self, request):
        planets = Planet.objects.all()
        data = [{
            "name": p.name,
            "species":p.species,
            "total_plasmators": p.plasmators
        } for p in planets]

        data = sorted(data, key=lambda e: -e["total_plasmators"])[:10]

        for i, e in enumerate(data):
            e["rank"] = i + 1

        serializer = PlasmatorToplistSerializer(data, many=True)
        return Response(serializer.data)


class SpeciesToplistViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def list(self, request):
        results = []

        for s in Species.objects.all().values_list("name", flat=True):
            qs = Planet.objects.filter(species=s).order_by("-points")
            if qs.exists():
                top = qs.first()
                results.append({
                    "species": s,
                    "name": top.name,
                    "points": top.points,
                })
            else:
                results.append({
                    "species": s,
                    "name": "-",
                    "points": 0,
                })

        # Sort species by points but keep them all
        results = sorted(results, key=lambda e: -e["points"])

        for i, row in enumerate(results):
            row["rank"] = i + 1

        serializer = SpeciesToplistSerializer(results, many=True)
        return Response(serializer.data)


class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [NewsAuthorOrReadOnly]  # Custom permission class
    lookup_field = 'slug'

    def perform_create(self, serializer):
        # Automatically associate the news author with the user's planet
        planet = Planet.objects.get(user=self.request.user)
        round = Round.objects.all().order_by("number").last()
        serializer.save(author=planet, round=round.number, turn=round.turn)


class EncyclopediaViewSet(viewsets.ModelViewSet):
    queryset = Encyclopedia.objects.all()
    serializer_class = EncyclopediaSerializer
    lookup_field = 'slug'
    
    def get_permissions(self):
        # Apply different permissions based on the request method
        if self.request.method not in SAFE_METHODS:
            return [IsAdminUser()]
        else:
            return [AllowAny()]

# Private Viewsets

from rest_framework.decorators import action
from django.shortcuts import get_object_or_404

class PlanetDataViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        planet = Planet.objects.get(user=request.user)
        serializer = PlanetDataSerializer(planet)
        return Response(serializer.data)
        
    @action(detail=False, methods=["get"], url_path="me")
    def me(self, request):
        planet = Planet.objects.get(user=request.user)
        serializer = PlanetDataSerializer(planet, context={"request": request})
        return Response(serializer.data)

    @action(detail=False, methods=["get"], url_path=r"(?P<x>\d+)/(?P<y>\d+)/(?P<z>\d+)")
    def by_coordinates(self, request, x, y, z):
        try:
            planet = Planet.objects.get(x=x, y=y, z=z)
        except Planet.DoesNotExist:
            return Response({"detail": "Planet not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = PlanetDataSerializer(planet, context={"request": request})
        return Response(serializer.data)

    @action(detail=False, methods=["get"], url_path=r"(?P<x>\d+)/(?P<y>\d+)/(?P<z>\d+)/next")
    def next(self, request, x=None, y=None, z=None):
        try:
            next_planet = Planet.objects.filter(x=x, y=y, z__gt=z).order_by('z').first()
            if not next_planet:
                next_planet = Planet.objects.filter(x=x, y__gt=y).order_by('y','z').first()
            if not next_planet:
                next_planet = Planet.objects.filter(x__gt=x).order_by('x','y','z').first()
            if not next_planet:
                return Response({'detail': 'No next planet.'}, status=404)
            serializer = PlanetDataSerializer(next_planet)
            return Response(serializer.data)
        except Planet.DoesNotExist:
            return Response({'detail': 'Current planet not found.'}, status=404)

    @action(detail=False, methods=["get"], url_path=r"(?P<x>\d+)/(?P<y>\d+)/(?P<z>\d+)/previous")
    def previous(self, request, x=None, y=None, z=None):
        try:
            prev_planet = Planet.objects.filter(x=x, y=y, z__lt=z).order_by('-z').first()
            if not prev_planet:
                prev_planet = Planet.objects.filter(x=x, y__lt=y).order_by('-y','-z').first()
            if not prev_planet:
                prev_planet = Planet.objects.filter(x__lt=x).order_by('-x','-y','-z').first()
            if not prev_planet:
                return Response({'detail': 'No previous planet.'}, status=404)
            serializer = PlanetDataSerializer(prev_planet)
            return Response(serializer.data)
        except Planet.DoesNotExist:
            return Response({'detail': 'Current planet not found.'}, status=404)

    @action(detail=False, methods=['post'], url_path='profile', parser_classes=[MultiPartParser, FormParser])
    def update_profile(self, request):
        try:
            planet = Planet.objects.get(user=request.user)
        except Planet.DoesNotExist:
            return Response({"detail": "Planet not found."}, status=status.HTTP_404_NOT_FOUND)

        slogan = request.data.get('slogan')
        if slogan:
            planet.slogan = slogan[:256]

        if 'profile_image' in request.FILES:
            planet.profile_image = request.FILES['profile_image']

        planet.save()
        return Response({'message': 'Profile updated successfully.'}, status=status.HTTP_200_OK)
        
        
class PDSViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        # Get the planet owned by the user
        planet = Planet.objects.get(user=request.user)
        
        # Get fleets that are based on the planet and owned by the user
        fleets = Fleet.objects.filter(base=True, owner=planet)
        
        # Get PDS (Planetary Defense Systems) ships from these fleets
        pds = Ship.objects.filter(fleet__in=fleets, ship_model__pds=True)
        
        exc_spec = ["Digitrox"]
        species = planet.species if planet.species in exc_spec else "Global"
        
        pds_models = ShipModel.objects.filter(pds=True, species=species).order_by("initiative")
        
        data = []
        for pds_model in pds_models:
            p = pds.filter(ship_model=pds_model)
            if p:
                data.append({"id":pds_model.id, "name":pds_model.name, "quantity":sum(p.values_list("quantity", flat=True))})
            else:
                data.append({"id":pds_model.id, "name":pds_model.name, "quantity":0})
        
        # Serialize the queryset with many=True since we're serializing multiple objects
        serializer = PDSSerializer(data, many=True)
        
        return Response(serializer.data)


class AvailablePDSViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        # Get the planet owned by the user
        planet = Planet.objects.get(user=request.user)

        exc_spec = ["Digitrox"]
        species = planet.species if planet.species in exc_spec else "Global"

        prs = PlanetResearch.objects.filter(planet=planet, completed=True)
        srs = SolResearch.objects.filter(sol=planet.sol, completed=True)
        ars = AllianceResearch.objects.filter(alliance=planet.alliance, completed=True)
        
        pds_models = ShipModel.objects.filter(pds=True, species=species).order_by("initiative")
        data = []
        for pds_model in pds_models:
            active = False
            research = pds_model.requirement
            if research:
                pr = prs.filter(research=research)
                sr = srs.filter(research=research)
                ar = None
                if planet.alliance:
                    ar = ars.filter(research=research)
                if pr or sr or ar:
                    active = True
            else:
                active = True
            data.append({"id":pds_model.id, "name":pds_model.name, "active":active})

        serializer = AvailablePDSSerializer(data, many=True)
        
        return Response(serializer.data)


class SatelliteViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        stocked_satellites = StockedSatellite.objects.filter(planet__user=request.user)
                
        data = []
        for satellite in SatelliteType.objects.all().order_by("production_time"):
            s = stocked_satellites.filter(satellite_type=satellite)
            if s:
                data.append({"id":satellite.id, "name":satellite.name, "quantity":sum(s.values_list("quantity", flat=True))})
            else:
                data.append({"id":satellite.id, "name":satellite.name, "quantity":0})
        
        serializer = SatelliteSerializer(data, many=True)
        
        return Response(serializer.data)

class AvailableSatelliteViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        # Get the planet owned by the user
        planet = Planet.objects.get(user=request.user)

        prs = PlanetResearch.objects.filter(planet=planet, completed=True)
        srs = SolResearch.objects.filter(sol=planet.sol, completed=True)
        ars = AllianceResearch.objects.filter(alliance=planet.alliance, completed=True)
        
        data = []
        for satellite in SatelliteType.objects.all().order_by("production_time"):
            active = False
            research = satellite.requirement
            if research:
                pr = prs.filter(research=research)
                sr = srs.filter(research=research)
                ar = None
                if planet.alliance:
                    ar = ars.filter(research=research)
                if pr or sr or ar:
                    active = True
            else:
                active = True
            data.append({"id":satellite.id, "name":satellite.name, "active":active})

        serializer = AvailableSatelliteSerializer(data, many=True)
        
        return Response(serializer.data)


class ShipViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        planet = Planet.objects.get(user=request.user)
        
        fleets = Fleet.objects.filter(owner=planet)
        
        ships = Ship.objects.filter(fleet__in=fleets, ship_model__pds=False)
        
        species = [planet.species, "Global", "Extra"]
        
        ship_models = ShipModel.objects.filter(pds=False, species__in=species).order_by("initiative")
        
        data = []
        for ship_model in ship_models:
            s = ships.filter(ship_model=ship_model)
            if s:
                data.append({"id":ship_model.id, "name":ship_model.name, "ship_class":ship_model.ship_class, "quantity":sum(s.values_list("quantity", flat=True))})
            else:
                data.append({"id":ship_model.id, "name":ship_model.name, "ship_class":ship_model.ship_class, "quantity":0})
        
        serializer = ShipSerializer(data, many=True)
        
        return Response(serializer.data)

class AvailableShipViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        planet = Planet.objects.get(user=request.user)

        species = [planet.species, "Global", "Extra"]
        
        prs = PlanetResearch.objects.filter(planet=planet, completed=True)
        srs = SolResearch.objects.filter(sol=planet.sol, completed=True)
        ars = AllianceResearch.objects.filter(alliance=planet.alliance, completed=True)
        
        ship_models = ShipModel.objects.filter(pds=False, species__in=species).order_by("initiative")
        data = []
        for ship_model in ship_models:
            active = False
            research = ship_model.requirement
            if research:
                pr = prs.filter(research=research)
                sr = srs.filter(research=research)
                ar = None
                if planet.alliance:
                    ar = ars.filter(research=research)
                if pr or sr or ar:
                    active = True
            else:
                active = True
            data.append({"id":ship_model.id, "name":ship_model.name, "active":active})

        serializer = AvailableShipSerializer(data, many=True)
        
        return Response(serializer.data)



class FleetViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        planet = Planet.objects.get(user=request.user)
        fleets = Fleet.objects.filter(owner=planet, base=False)

        serializer = FleetSerializer(fleets, many=True)
        return Response(serializer.data)


class ResearchViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        research = PlanetResearch.objects.filter(planet__user=request.user)
        serializer = PlanetResearchSerializer(research, many=True)
        return Response(serializer.data)


# Permissions to ensure user can only access their own messages
class IsMessageOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.sender.user == request.user or obj.receiver.user == request.user

class ReceivedMessagesViewSet(ViewSet):
    """
    A ViewSet for listing received messages.
    """
    permission_classes = [IsAuthenticated]

    def list(self, request):
        try:
            planet = Planet.objects.get(user=request.user)
        except Planet.DoesNotExist:
            return Response({"detail": "Planet not found."}, status=status.HTTP_404_NOT_FOUND)

        # Retrieve received messages for the authenticated user
        messages = Message.objects.filter(receiver=planet).order_by('-server_time')
        serializer = MessageListSerializer(messages, many=True)
        return Response(serializer.data)
        

class SentMessagesViewSet(ViewSet):
    """
    A ViewSet for listing sent messages.
    """
    permission_classes = [IsAuthenticated]

    def list(self, request):
        try:
            planet = Planet.objects.get(user=request.user)
        except Planet.DoesNotExist:
            return Response({"detail": "Planet not found."}, status=status.HTTP_404_NOT_FOUND)

        # Retrieve sent messages for the authenticated user
        messages = Message.objects.filter(sender=planet).order_by('-server_time')
        serializer = MessageListSerializer(messages, many=True)
        return Response(serializer.data)


class ReadMessageViewSet(ViewSet):
    """
    A ViewSet for retrieving and marking a message as read.
    """
    permission_classes = [IsAuthenticated, IsMessageOwner]

    def retrieve(self, request, pk=None):
        """
        Retrieve a single message by its ID and mark it as read.
        """
        try:
            # Get the message by ID and ensure the user is the sender or receiver
            message = Message.objects.get(pk=pk)
            if not (message.sender.user == request.user or message.receiver.user == request.user):
                raise PermissionDenied("You do not have permission to view this message.")
            
            # Mark the message as read
            if not message.read:
                message.read = True
                message.save()

            # Serialize the message details
            serializer = MessageDetailSerializer(message)
            return Response(serializer.data)
        except Message.DoesNotExist:
            return Response({"detail": "Message not found."}, status=404)


class CommunicationViewSet(ViewSet):
    """
    A ViewSet for fetching unread notifications and messages counts.
    """
    permission_classes = [IsAuthenticated]

    def list(self, request):
        """
        Returns the count of unread notifications and messages for the authenticated user.
        """
        planet = Planet.objects.get(user=request.user)

        # Count unread notifications and messages
        new_events = Notification.objects.filter(planet=planet, read=False).count()
        new_messages = Message.objects.filter(receiver=planet, read=False).count()

        # Serialize and return the response
        data = {
            "new_events": new_events,
            "new_messages": new_messages,
        }
        serializer = CommunicationSerializer(data)
        return Response(serializer.data)
        

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import MinistersMessageSerializer

class MinistersMessageViewSet(viewsets.ViewSet):
    """
    ViewSet for managing the ministers' message in a Sol.
    """
    permission_classes = [IsAuthenticated]

    def list(self, request):
        """
        GET /api/v1/ministers-message/
        Returns the ministers' message of the authenticated user's Sol.
        """
        try:
            planet = Planet.objects.get(user=request.user)
            sol = planet.sol
        except Planet.DoesNotExist:
            return Response({"detail": "Planet not found."}, status=status.HTTP_404_NOT_FOUND)

        if not sol:
            return Response({"detail": "Sol not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = MinistersMessageSerializer(sol)
        return Response(serializer.data)


from .serializers import AllianceNewsSerializer

class AllianceNewsViewSet(viewsets.ViewSet):
    """
    ViewSet for managing the Alliance News.
    """
    permission_classes = [IsAuthenticated]

    def list(self, request):
        """
        GET /api/v1/alliance-news/
        Returns the news of the authenticated user's Alliance.
        """
        try:
            planet = Planet.objects.get(user=request.user)
            alliance = planet.alliance
        except Planet.DoesNotExist:
            return Response({"detail": "Planet not found."}, status=status.HTTP_404_NOT_FOUND)

        if not alliance:
            return Response({"detail": "Alliance not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = AllianceNewsSerializer(alliance)
        return Response(serializer.data)


from .serializers import LatestNewsSerializer

class LatestNewsViewSet(viewsets.ViewSet):
    """
    ViewSet for managing the Latest News.
    """
    permission_classes = [IsAuthenticated]

    def list(self, request):
        """
        GET /api/v1/latest-news/
        Returns the news of the authenticated user's Alliance.
        """
        news = News.objects.order_by("server_time").last()

        serializer = LatestNewsSerializer(news)
        return Response(serializer.data)
        

from .serializers import HomeTechnologySerializer

class HomeTechnologyViewSet(viewsets.ViewSet):
    """
    ViewSet for the home page's technology section. It only list the active researches.
    """
    permission_classes = [IsAuthenticated]

    def list(self, request):
        """
        GET /api/v1/home-technology/
        Returns the active researches.
        """
        try:
            planet = Planet.objects.get(user=request.user)
        except Planet.DoesNotExist:
            return Response({"detail": "Planet not found."}, status=status.HTTP_404_NOT_FOUND)

        researches = PlanetResearch.objects.filter(planet=planet, started=True, completed=False) 

        research = researches.filter(research__building=False).last()
        building = researches.filter(research__building=True).last()
        
        # Serialize and return the response
        data = {
            "research": None if not research else research.research.name,
            "research_turns": None if not research else research.turns_remaining,
            "building": None if not building else building.research.name,
            "building_turns": None if not building else building.turns_remaining,
        }
        serializer = HomeTechnologySerializer(data)
        return Response(serializer.data)
        
        
from .serializers import PlasmatorSerializer

class PlasmatorViewSet(viewsets.ViewSet):
    """
    ViewSet for managing own plasmators.
    """
    permission_classes = [IsAuthenticated]

    def list(self, request):
        """
        GET /api/v1/plasmators/
        Returns the plasmators of the authenticated user.
        """
        try:
            planet = Planet.objects.get(user=request.user)
        except Planet.DoesNotExist:
            return Response({"detail": "Planet not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = PlasmatorSerializer(planet)
        return Response(serializer.data)
        
        
class SolIncomingViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        planet = Planet.objects.get(user=request.user)

        serializer = IncomingSerializer(planet.sol.incoming_fleets, many=True)
        return Response(serializer.data)

        
class SolOutgoingViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        planet = Planet.objects.get(user=request.user)

        serializer = OutgoingSerializer(planet.sol.outgoing_fleets, many=True)
        return Response(serializer.data)


class AllianceIncomingViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        planet = Planet.objects.get(user=request.user)

        serializer = IncomingSerializer(planet.alliance.incoming_fleets, many=True)
        return Response(serializer.data)

class AllianceOutgoingViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        planet = Planet.objects.get(user=request.user)

        serializer = OutgoingSerializer(planet.alliance.outgoing_fleets, many=True)
        return Response(serializer.data)


class TechTreeViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        planet = Planet.objects.get(user=request.user)
        researches = Research.objects.filter(Q(species=planet.species) | Q(species="common"))
        p_researches = PlanetResearch.objects.filter(planet=planet)
        if researches.count() > p_researches.count():
            for e in researches.exclude(id__in=p_researches.values_list("research", flat=True)):
                pr, c = PlanetResearch.objects.get_or_create(planet=planet, research=e)
            p_researches = PlanetResearch.objects.filter(planet=planet)
        serializer = TechTreeSerializer(p_researches, many=True)
        return Response(serializer.data)
        

class ResourceProductionViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        """
        GET /api/v1/resource-production/
        """
        try:
            planet = Planet.objects.get(user=request.user)
        except Planet.DoesNotExist:
            return Response({"detail": "Planet not found."}, status=status.HTTP_404_NOT_FOUND)


        data = {
            "metal": {
                "amount": planet.metal_plasmator,
                "plasmator_income": planet.gross_metal_production - planet.planet_metal_production,
                "planet_income": planet.planet_metal_production,
                "minister": planet.production_minister_bonus,
                "tax": planet.metal_tax,
                "net_income": planet.net_metal_production,
                "gross_income": planet.gross_metal_production,
            },

            "crystal": {
                "amount": planet.crystal_plasmator,
                "plasmator_income": planet.gross_crystal_production - planet.planet_crystal_production,
                "planet_income": planet.planet_crystal_production,
                "minister": 0,
                "tax": planet.crystal_tax,
                "net_income": planet.net_crystal_production,
                "gross_income": planet.gross_crystal_production,
            },

            "narion": {
                "amount": planet.narion_plasmator,
                "plasmator_income": planet.gross_narion_production - planet.planet_narion_production,
                "planet_income": planet.planet_narion_production,
                "minister": 0,
                "tax": planet.narion_tax,
                "net_income": planet.net_narion_production,
                "gross_income": planet.gross_narion_production,
            },

            "neutral": {
                "amount": planet.neutral_plasmator,
                "plasmator_income": 0,
                "planet_income": 0,
                "minister": 0,
                "tax": 0,
                "net_income": 0,
                "gross_income": 0,
            },
        }
        serializer = ResourceProductionSerializer(data)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='plasmator-probes')
    def plasmator_probes(self, request):
        from engine.models import SatelliteType
        satellite = SatelliteType.objects.get(code="plasmator")
        s = StockedSatellite.objects.filter(planet__user=request.user, satellite_type=satellite)
                
        data = []
        if s:
            data.append({"id":satellite.id, "name":satellite.name, "quantity":sum(s.values_list("quantity", flat=True))})
        else:
            data.append({"id":satellite.id, "name":satellite.name, "quantity":0})
        
        serializer = SatelliteSerializer(data, many=True)
        
        return Response(serializer.data)
        
    @action(detail=False, methods=['post'], url_path='launch')
    def launch(self, request):
        planet = Planet.objects.get(user=self.request.user)
        new_plasmators = planet.plasmator_probing(quantity=request.data.get('quantity'))
        return Response({
            "status": "launching successful",
            "new_plasmators": new_plasmators,
        })

from rest_framework import viewsets
from rest_framework.decorators import action
from engine.models import ShipModel, ShipProduction
from .serializers import  ProduceSerializer
from django.db.models import Sum

class ShipProductionViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def available(self, request, pds=False):
        try:
            planet = Planet.objects.get(user=request.user)
        except Planet.DoesNotExist:
            return Response({"detail": "Planet not found."}, status=status.HTTP_404_NOT_FOUND)
        species = planet.species
        qs = ShipModel.objects.filter(Q(species=species) | Q(species='Extra')).filter(
            pds=pds).order_by('species', 'initiative')
        serializer = ProductionShipModelSerializer(qs, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='available')
    def ship_available(self, request):
        return self.available(request)

    @action(detail=False, methods=['get'], url_path='pds-available')
    def pds_available(self, request):
        return self.available(request, pds=True)

    @action(detail=False, methods=['post'], url_path='produce')
    def produce(self, request):
        serializer = ProduceSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        try:
            planet = Planet.objects.get(user=request.user)
        except Planet.DoesNotExist:
            return Response({"detail": "Planet not found."}, status=status.HTTP_404_NOT_FOUND)
        for item in serializer.validated_data:
            ship_model = ShipModel.objects.get(pk=item['ship_model'])
            if ship_model.can_produce(planet):
                ShipProduction.objects.create(
                    planet=planet,
                    ship_model=ship_model,
                    quantity=item['quantity'],
                    turns_remaining=ship_model.production_time
                )
        return Response({'message': 'Production started'}, status=status.HTTP_201_CREATED)


    def production_line(self, request, pds=False):
        try:
            planet = Planet.objects.get(user=request.user)
        except Planet.DoesNotExist:
            return Response({"detail": "Planet not found."}, status=status.HTTP_404_NOT_FOUND)

        productions = (
            ShipProduction.objects
            .filter(planet=planet, turns_remaining__lte=16, ship_model__pds=pds)
            .values('ship_model__name', 'turns_remaining')
            .annotate(quantity=Sum('quantity'))
            .order_by('ship_model__species', 'ship_model__initiative')
        )

        data = {}
        for entry in productions:
            name = entry['ship_model__name']
            turn = entry['turns_remaining']
            qty = entry['quantity']
            if name not in data:
                data[name] = {str(t): 0 for t in range(1, 17)}
            data[name][str(turn)] = qty

        return Response(data)

    @action(detail=False, methods=['get'], url_path='line')
    def ship_production_line(self, request):
        return self.production_line(request)

    @action(detail=False, methods=['get'], url_path='pds-line')
    def pds_production_line(self, request):
        return self.production_line(request, pds=True)


from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from engine.models import ShipModel
from game.serializers import ShipScrapSerializer, ShipOwnedSerializer

class ShipScrapViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def owned(self, request, pds=False):
        planet = get_object_or_404(Planet, user=request.user)
        base_fleet = Fleet.objects.filter(owner=planet, base=True).first()
        ships = Ship.objects.filter(fleet=base_fleet, ship_model__pds=pds)
        serializer = ShipOwnedSerializer(ships, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='owned')
    def ship_owned(self, request):
        return self.owned(request)

    @action(detail=False, methods=['get'], url_path='pds-owned')
    def pds_owned(self, request):
        return self.owned(request, pds=True)

    @action(detail=False, methods=['post'], url_path='scrap')
    def scrap(self, request):
        serializer = ShipScrapSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        planet = get_object_or_404(Planet, user=request.user)
        base_fleet = Fleet.objects.filter(owner=planet, base=True).first()

        ship = get_object_or_404(Ship, fleet=base_fleet, ship_model_id=serializer.validated_data['ship_model'])
        quantity = serializer.validated_data['quantity']
        materials = ship.scrap(quantity)

        return Response({'message': 'Scrapped successfully', 'gained': materials})


from engine.models import SatelliteProduction
from game.serializers import SatelliteTypeSerializer, ProduceSatelliteSerializer
from rest_framework.permissions import IsAuthenticated

class SatelliteProductionViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'], url_path='available')
    def available(self, request):
        planet = Planet.objects.get(user=request.user)

        qs = SatelliteType.objects.all()
        serializer = SatelliteTypeSerializer(qs, many=True, context={'planet': planet})
        return Response(serializer.data)

    @action(detail=False, methods=['post'], url_path='produce')
    def produce(self, request):
        serializer = ProduceSatelliteSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)

        planet = Planet.objects.get(user=request.user)

        for item in serializer.validated_data:
            SatelliteProduction.objects.create(
                planet=planet,
                satellite_type=item['satellite_type'],
                quantity=item['quantity'],
                turns_remaining=item['satellite_type'].production_time
            )

        return Response({"message": "Production started"}, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'], url_path='line')
    def line(self, request):
        planet = Planet.objects.get(user=request.user)

        productions = (
            SatelliteProduction.objects
            .filter(planet=planet, turns_remaining__lte=16)
            .values('satellite_type__name', 'turns_remaining')
            .annotate(quantity=Sum('quantity'))
            .order_by('satellite_type__production_time')
        )

        data = {}
        for entry in productions:
            name = entry['satellite_type__name']
            turn = entry['turns_remaining']
            qty = entry['quantity']
            if name not in data:
                data[name] = {str(t): 0 for t in range(1, 17)}
            data[name][str(turn)] = qty

        return Response(data)

    @action(detail=False, methods=['get'], url_path='scrappable')
    def scrappable(self, request):
        planet = Planet.objects.get(user=request.user)
        satellites = StockedSatellite.objects.filter(planet=planet)
        data = [
            {
                'id': s.id,
                'name': s.satellite_type.name,
                'quantity': s.quantity,
                'metal': s.satellite_type.metal,
                'crystal': s.satellite_type.crystal,
                'narion': s.satellite_type.narion
            }
            for s in satellites
        ]
        return Response(data)

    @action(detail=False, methods=['post'], url_path='scrap')
    def scrap(self, request):
        sat_id = request.data.get('satellite_type')
        qty = int(request.data.get('quantity', 0))
        try:
            stock = StockedSatellite.objects.get(satellite_type__id=sat_id, planet__user=request.user)
        except StockedSatellite.DoesNotExist:
            return Response({'detail': 'Not found'}, status=404)

        if qty > stock.quantity:
            return Response({'detail': 'Not enough quantity'}, status=400)

        # Add 10% back to planet
        satellite_type = stock.satellite_type
        planet = stock.planet
        planet.metal += int(satellite_type.metal * qty * 0.5)
        planet.crystal += int(satellite_type.crystal * qty * 0.5)
        planet.narion += int(satellite_type.narion * qty * 0.5)
        planet.save()

        stock.quantity -= qty
        stock.save()

        return Response({'message': 'Scrapped'})


from .serializers import FleetNameSerializer

class FleetSettingsViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        fleets = Fleet.objects.filter(owner__user=request.user, base=False).order_by('id')
        serializer = FleetNameSerializer(fleets, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], url_path='update-names')
    def update_names(self, request):
        fleets = Fleet.objects.filter(owner__user=request.user).order_by('id')
        data = request.data

        for fleet in fleets:
            fleet_name = data.get(str(fleet.id), None)
            if fleet_name:
                fleet.name = fleet_name
                fleet.save()

        return Response({'message': 'Fleet names updated'})
        

from .serializers import FleetFormationSerializer

class FleetStrategyViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        fleets = Fleet.objects.filter(owner__user=request.user, base=False).order_by('id')
        serializer = FleetFormationSerializer(fleets, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], url_path='update-strategy')
    def update_formations(self, request):
        fleets = Fleet.objects.filter(owner__user=request.user, base=False).order_by('id')
        data = request.data

        for fleet in fleets:
            formation = data.get(str(fleet.id), None)
            if formation in ['wedge', 'wall', 'sphere']:
                fleet.formation = formation
                fleet.save()

        return Response({'message': 'Fleet formations updated'})

from .serializers import FleetControlSerializer

class FleetControlViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        planet = Planet.objects.get(user=request.user)
        fleets = Fleet.objects.filter(owner=planet, base=False).order_by('id')
        serializer = FleetControlSerializer(fleets, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def task(self, request, pk=None):
        fleet = Fleet.objects.get(id=pk, owner__user=request.user)
        if fleet.task in ("move","return"):
            return Response({'detail': 'Cannot issue task to a moving fleet.'}, status=400)

        action_type = request.data.get('action')[:-1]
        target_x = request.data.get('x')
        target_y = request.data.get('y')
        target_z = request.data.get('z')
        turns = int(request.data.get('action', '1')[-1:])
        

        try:
            target = Planet.objects.get(x=target_x, y=target_y, z=target_z)
        except Planet.DoesNotExist:
            return Response({'detail': 'Target planet not found.'}, status=404)

        if action_type == "attack":
            fleet.attack(turns, target)
        elif action_type == "defend":
            fleet.defend(turns, target)
        else:
            return Response({'detail': 'Invalid action.'}, status=400)

        return Response({'message': 'Fleet task assigned.'})

    @action(detail=True, methods=['post'])
    def callback(self, request, pk=None):
        fleet = Fleet.objects.get(id=pk, owner__user=request.user)
        fleet.callback()
        return Response({'message': 'Fleet recalled.'})


    @action(detail=False, methods=['get'], url_path='fuel-costs')
    def fuel_costs(self, request):
        fleets = Fleet.objects.filter(owner__user=request.user, base=False).order_by('id')
        distances = [*map(lambda e:e.distances, fleets)]
        
        data = []
        for m, d in enumerate(('sol','gal','uni'), start=1):
            row = {"name": d}
            travel = "travel_" + d
            for i, fleet in enumerate(fleets, start=1):
                row[f"fleet{i}_fuel"] = fleet.fuel_cost * m
                row[f"fleet{i}_distance"] = distances[i-1][travel]
            data.append(row)

        return Response(data)
        
        
    @action(detail=False, methods=['get'], url_path='ships')
    def ships(self, request):
        planet = Planet.objects.get(user=request.user)

        # Get all fleets for the user (planet)
        fleets = Fleet.objects.filter(owner=planet).order_by('-base','id')

        # Collect ships
        ships_data = []
        ships = Ship.objects.filter(fleet__in=fleets, quantity__gt=0, ship_model__pds=False)
        models = set(ships.values_list('ship_model', flat=True))
        all_ship_models = ShipModel.objects.filter(id__in=models)

        for model in all_ship_models:
            ships_data.append({
                'id': model.id,
                'name': model.name,
                'ship_class': model.ship_class,
                'target1': model.target1,
                'target2': model.target2,
                'target3': model.target3,
                'base': sum(ships.filter(fleet=fleets[0], ship_model=model).values_list('quantity', flat=True)),
                'fleet1': sum(ships.filter(fleet=fleets[1], ship_model=model).values_list('quantity', flat=True)),
                'fleet2': sum(ships.filter(fleet=fleets[2], ship_model=model).values_list('quantity', flat=True)),
                'fleet3': sum(ships.filter(fleet=fleets[3], ship_model=model).values_list('quantity', flat=True)),
                'fleet4': sum(ships.filter(fleet=fleets[4], ship_model=model).values_list('quantity', flat=True)),

                'base_id': fleets[0].id,
                'fleet1_id': fleets[1].id,
                'fleet2_id': fleets[2].id,
                'fleet3_id': fleets[3].id,
                'fleet4_id': fleets[4].id,
            })

        serializer = FleetsShipModelSerializer(ships_data, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], url_path='swap-ship')
    def swap_ship(self, request):
        planet = Planet.objects.get(user=request.user)
        source_fleet_id = request.data.get('source_fleet_id')
        target_fleet_id = request.data.get('target_fleet_id')
        ship_model_id = request.data.get('ship_model_id')
        quantity = int(request.data.get('quantity', 0))

        if source_fleet_id is None or target_fleet_id is None or ship_model_id is None or quantity <= 0:
            return Response({'detail': 'Invalid input.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            source_fleet = Fleet.objects.get(id=source_fleet_id, owner=planet)
            target_fleet = Fleet.objects.get(id=target_fleet_id, owner=planet)
            ship_model = ShipModel.objects.get(id=ship_model_id)
        except (Fleet.DoesNotExist, ShipModel.DoesNotExist):
            return Response({'detail': 'Fleet or ship model not found.'}, status=status.HTTP_404_NOT_FOUND)

        source_fleet.swap_ship(target_fleet, ship_model, quantity)

        return Response({'message': 'Ship transfer successful.'})

    @action(detail=False, methods=['get'], url_path='fleet-list')
    def fleet_list(self, request):
        planet = Planet.objects.get(user=request.user)
        fleets = Fleet.objects.filter(owner=planet).order_by('-base','id')
        serializer = FcFleetListSerializer(fleets, many=True)
        return Response(serializer.data)

    
from rest_framework import filters

from engine.models import ProbeReport
from .serializers import ProbeReportSerializer

from rest_framework.pagination import PageNumberPagination

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

class ExploringViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProbeReportSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['server_time']
    ordering = ['-server_time']
    search_fields = ['probe_type']
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        sender_planet = Planet.objects.get(user=self.request.user)
        queryset = ProbeReport.objects.filter(sender_planet=sender_planet).order_by('-server_time')
        probe_type = self.request.query_params.get('probe_type')
        if probe_type:
            queryset = queryset.filter(probe_type=probe_type)
        return queryset


    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def launch_probe(self, request):
        from engine.models import Notification
        data = request.data

        sender_planet = Planet.objects.get(user=request.user)
        try:
            target_planet = Planet.objects.get(x=data['x'], y=data['y'], z=data['z'])
        except Planet.DoesNotExist:
            return Response({"detail": "Planet not found."}, status=status.HTTP_404_NOT_FOUND)

        probe = SatelliteType.objects.get(code=data["probe_type"])
        result = target_planet.probing(sender=sender_planet, probe=probe, quantity=data["quantity"])
        if result:
            current_round = Round.objects.all().order_by("number").last()

            report = ProbeReport.objects.create(
                probe_type = data['probe_type'],
                sender_planet = sender_planet,
                target_planet = target_planet,
                round = current_round.number,
                turn = current_round.turn,
                result_json = result,
            )
            
            Notification.objects.create(
                ntype = "Probe",
                planet = target_planet,
                round = current_round.number,
                turn = current_round.turn,
                content = {"report" : "The sensors detected probes. The type and origin of the probes are unknown."}
            )
            
            return Response({
                "status": "probe launched",
                "report_id": report.id
            }, status=status.HTTP_201_CREATED)
        
from .serializers import NotificationSerializer

class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['server_time']
    ordering = ['-server_time']
    search_fields = ['ntype']
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        planet = Planet.objects.get(user=self.request.user)
        queryset = Notification.objects.filter(planet=planet).order_by('-server_time')
        ntype = self.request.query_params.get('ntype')
        if ntype:
            queryset = queryset.filter(ntype=ntype)
        return queryset
        

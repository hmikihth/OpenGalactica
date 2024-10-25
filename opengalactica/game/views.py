from django.utils.timezone import now

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAdminUser, SAFE_METHODS

from engine.models import Species, ShipModel, Alliance, Sol, Planet, News, Encyclopedia
from engine.models import StockedSatellite, SatelliteType, Ship, Fleet, Research, Round
from engine.models import PlanetResearch, SolResearch, AllianceResearch

from game.permissions import NewsAuthorOrReadOnly
from game.serializers import EncyclopediaSerializer


from game.serializers import (
    TimeSerializer, SpeciesSerializer, ShipModelSerializer, AllianceToplistSerializer, 
    SolToplistSerializer, PlanetToplistSerializer, NewsSerializer,# EncyclopediaSerializer,
    PlanetDataSerializer, PDSSerializer, AvailablePDSSerializer, SatelliteSerializer, AvailableSatelliteSerializer,
    ShipSerializer, AvailableShipSerializer, FleetSerializer, ResearchSerializer
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
        data = [{"name": p.name, "alliance": str(p.alliance), "points": p.points} for p in planets]
        data = sorted(data, key=lambda e:-e["points"])
        for i, e in enumerate(data):
            e["rank"] = i+1
        serializer = PlanetToplistSerializer(data, many=True)
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

class PlanetDataViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        planet = Planet.objects.get(user=request.user)
        serializer = PlanetDataSerializer(planet)
        return Response(serializer.data)


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
        planet = Planet.objects.get(user=request.user)

        stocked_satellites = StockedSatellite.objects.filter(planet__user=request.user)
                
        data = []
        for satellite in SatelliteType.objects.all().order_by("production_time"):
            s = stocked_satellites.filter(satellite=satellite)
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

        fleets = Fleet.objects.filter(owner=planet)

        ships = Ship.objects.filter(fleet__in=fleets, ship_model__pds=False)
        
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
        serializer = ResearchSerializer(research, many=True)
        return Response(serializer.data)


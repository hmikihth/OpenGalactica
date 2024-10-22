from rest_framework.routers import DefaultRouter
from game.views import (
    TimeViewSet, SpeciesViewSet, ShipModelViewSet, AllianceToplistViewSet, 
    SolToplistViewSet, PlanetToplistViewSet, #NewsViewSet, EncyclopediaViewSet,
    PlanetDataViewSet, PDSViewSet, AvailablePDSViewSet, SatelliteViewSet, AvailableSatelliteViewSet,
    ShipViewSet, AvailableShipViewSet, FleetViewSet, ResearchViewSet
)

router = DefaultRouter()

# Public Endpoints
router.register(r'time', TimeViewSet, basename='time')
router.register(r'species', SpeciesViewSet, basename='species')
router.register(r'ship-models', ShipModelViewSet, basename='ship-models')
router.register(r'toplist/alliance', AllianceToplistViewSet, basename='alliance-toplist')
router.register(r'toplist/sol', SolToplistViewSet, basename='sol-toplist')
router.register(r'toplist/planet', PlanetToplistViewSet, basename='planet-toplist')
#router.register(r'news', NewsViewSet, basename='news')
#router.register(r'encyclopedia', EncyclopediaViewSet, basename='encyclopedia')

# Private Endpoints
router.register(r'planet', PlanetDataViewSet, basename='planet')
router.register(r'pds', PDSViewSet, basename='pds')
router.register(r'avpds', AvailablePDSViewSet, basename='avpds')
router.register(r'satellites', SatelliteViewSet, basename='satellites')
router.register(r'avsatellites', AvailableSatelliteViewSet, basename='avsatellites')
router.register(r'ships', ShipViewSet, basename='ships')
router.register(r'avships', AvailableShipViewSet, basename='avships')
router.register(r'fleets', FleetViewSet, basename='fleets')
router.register(r'research', ResearchViewSet, basename='research')

urlpatterns = router.urls

from django.urls import path
from rest_framework.routers import DefaultRouter
from game.views import (
    TimeViewSet, SpeciesViewSet, ShipModelViewSet, AllianceToplistViewSet, 
    SolToplistViewSet, PlanetToplistViewSet, NewsViewSet, EncyclopediaViewSet,
    PlanetDataViewSet, PDSViewSet, AvailablePDSViewSet, SatelliteViewSet, AvailableSatelliteViewSet,
    ShipViewSet, AvailableShipViewSet, FleetViewSet, ResearchViewSet,
    ReceivedMessagesViewSet, SentMessagesViewSet, ReadMessageViewSet,
    CommunicationViewSet, MinistersMessageViewSet, AllianceNewsViewSet, LatestNewsViewSet,
    HomeTechnologyViewSet, PlasmatorViewSet, 
    SolIncomingViewSet, SolOutgoingViewSet, AllianceIncomingViewSet, AllianceOutgoingViewSet,
    TechTreeViewSet, ResourceProductionViewSet, ShipProductionViewSet, ShipScrapViewSet, 
    SatelliteProductionViewSet, FleetSettingsViewSet, FleetStrategyViewSet, FleetControlViewSet,
    ExploringViewSet, NotificationViewSet
)


router = DefaultRouter()

# Public Endpoints
router.register(r'time', TimeViewSet, basename='time')
router.register(r'species', SpeciesViewSet, basename='species')
router.register(r'ship-models', ShipModelViewSet, basename='ship-models')
router.register(r'toplist/alliance', AllianceToplistViewSet, basename='alliance-toplist')
router.register(r'toplist/sol', SolToplistViewSet, basename='sol-toplist')
router.register(r'toplist/planet', PlanetToplistViewSet, basename='planet-toplist')
router.register(r'news', NewsViewSet, basename='news')
router.register(r'encyclopedia', EncyclopediaViewSet, basename='encyclopedia')

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

# Message Endpoints
router.register(r'messages/received', ReceivedMessagesViewSet, basename='received-messages')
router.register(r'messages/sent', SentMessagesViewSet, basename='sent-messages')
router.register(r'messages/read', ReadMessageViewSet, basename='read-message')

router.register(r'communication', CommunicationViewSet, basename='communication')
router.register(r'ministers-message', MinistersMessageViewSet, basename='ministers-message')
router.register(r'alliance-news', AllianceNewsViewSet, basename='alliance-news')
router.register(r'latest-news', LatestNewsViewSet, basename='latest-news')
router.register(r'home-technology', HomeTechnologyViewSet, basename='home-technology')
router.register(r'plasmators', PlasmatorViewSet, basename='plasmators')

router.register(r'sol/incoming', SolIncomingViewSet, basename='sol-incoming')
router.register(r'sol/outgoing', SolOutgoingViewSet, basename='sol-outgoing')

router.register(r'alliance/incoming', AllianceIncomingViewSet, basename='alliance-incoming')
router.register(r'alliance/outgoing', AllianceOutgoingViewSet, basename='alliance-outgoing')

router.register(r'techtree', TechTreeViewSet, basename='techtree')
router.register(r'resource-production', ResourceProductionViewSet, basename='resource-production')
router.register(r'ship-production', ShipProductionViewSet, basename='ship-production')
router.register(r'ship-scrap', ShipScrapViewSet, basename='ship-scrap')
router.register(r'satellite-production', SatelliteProductionViewSet, basename='satellite-production')

router.register(r'fleet-settings', FleetSettingsViewSet, basename='fleet-settings')
router.register(r'fleet-strategy', FleetStrategyViewSet, basename='fleet-strategy')
router.register(r'fleet-control', FleetControlViewSet, basename='fleet-control')
router.register(r'exploring', ExploringViewSet, basename='exploring')
router.register(r'notifications', NotificationViewSet, basename='notifications')


urlpatterns = [
    *router.urls,
]

from django.urls import path, include
from rest_framework import routers

from engine.views import ShipModelViewSet

router = routers.DefaultRouter()
router.register(r'ship-models', ShipModelViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
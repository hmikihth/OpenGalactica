from rest_framework import viewsets

from engine.models import ShipModel
from engine.serializers import ShipModelSerializer

class ShipModelViewSet(viewsets.ModelViewSet):
    queryset = ShipModel.objects.all()
    serializer_class = ShipModelSerializer
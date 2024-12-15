from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_list_or_404
from .models import Beer
from .serializers import BeerSerializer
from .permissions import IsBeerViewer, IsBeerEditor

# permissions
read_permissions = [IsBeerViewer]
write_permissions = [IsBeerEditor]

class BeerViewSet(viewsets.ModelViewSet):
    """
    A ViewSet to manage Beer instances.
    This ViewSet provides actions for different methods.
    """

    queryset = Beer.objects.all()
    serializer_class = BeerSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'get_beer_by_name']:
            return [permission() for permission in read_permissions]
        else:
            return [permission() for permission in write_permissions]

    @action(detail=False, methods=['get'], url_path='name')
    def get_beer_by_name(self, request, beer_name=None):
        beer = get_list_or_404(self.get_queryset(), name=beer_name)
        serializer = self.get_serializer(beer, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BreweryViewSet(viewsets.ViewSet):
    """
    A ViewSet to manage Brewery instances.
    This ViewSet provides actions for different methods.
    """

    def get_permissions(self):
        return [permission() for permission in read_permissions]


    @action(detail=False, methods=['get'], url_path='')
    def list_breweries(self, request):
        breweries = Beer.objects.values_list('brewery', flat=True).distinct()
        return Response(list(breweries), status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='count')
    def number_of_breweries(self, request):
        count = Beer.objects.values('brewery').distinct().count()
        return Response({"count": count}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'], url_path='beers')
    def get_beers_by_brewery(self, request, brewery_name=None):
        beers = Beer.objects.filter(brewery=brewery_name)
        serializer = BeerSerializer(beers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_list_or_404
from .models import Beer
from .serializers import BeerSerializer
from .permissions import IsBeerViewer, IsBeerEditor

# Permissions
read_permissions = [IsBeerViewer, IsAuthenticated]
write_permissions = [IsBeerEditor, IsAuthenticated]

class BeerViewSet(viewsets.ModelViewSet):
    """
    Basic CRUD methods.

    - Provides list, get, create, update, delete actions and allows retrieving beers by name.

    Permissions:
        - Read operations: Require `IsBeerViewer` permission.
        - Write operations: Require `IsBeerEditor` permission.
    """

    queryset = Beer.objects.all()
    serializer_class = BeerSerializer

    def get_permissions(self):
        """
        Set the permissions based on the action.
        """
        if self.action in ['list', 'retrieve', 'get_beer_by_name']:
            return [permission() for permission in read_permissions]
        return [permission() for permission in write_permissions]

    def get_beer_by_name(self, request, beer_name=None):
        """
        Retrieve beers by their name.

        Args:
            request (Request): The incoming HTTP request.
            beer_name (str): The name of the beer to retrieve.

        Returns:
            Response: HTTP 200 status with Beer Data
        """
        beers = self.queryset.filter(name__icontains=beer_name)
        serializer = self.get_serializer(beers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BreweryViewSet(viewsets.ViewSet):
    """
    A ViewSet to manage Brewery-related actions.

    This ViewSet provides actions to:
    - List all distinct breweries.
    - Count the total number of unique breweries.
    - Retrieve beers associated with a specific brewery.

    Permissions:
        - Requires `IsBeerViewer` permission for all actions.
    """

    def get_permissions(self):
        """
        Set permissions.
        """
        return [permission() for permission in read_permissions]


    @action(detail=False, methods=['get'], url_path='')
    def list_breweries(self, request):
        """
        List all distinct breweries.

        Args:
            request (Request): The incoming HTTP request.

        Returns:
            Response: HTTP 200 status with list of unique brewery names.
        """
        breweries = Beer.objects.values_list('brewery', flat=True).distinct()
        return Response(list(breweries), status=status.HTTP_200_OK)


    @action(detail=False, methods=['get'], url_path='count')
    def number_of_breweries(self, request):
        """
        Count the total number of unique breweries.

        Args:
            request (Request): The incoming HTTP request.

        Returns:
            Response: HTTP 200 status with the count of unique breweries.
        """
        count = Beer.objects.values('brewery').distinct().count()
        return Response({"count": count}, status=status.HTTP_200_OK)


    @action(detail=True, methods=['get'], url_path='beers')
    def get_beers_by_brewery(self, request, brewery_name=None):
        """
        Retrieve all beers associated with a specific brewery.

        Args:
            request (Request): The incoming HTTP request.
            brewery_name (str): The name of the brewery as base for the filter.

        Returns:
            Response: HTTP 200 status with all beers for the specified brewery.
        """
        beers = Beer.objects.filter(brewery=brewery_name)
        serializer = BeerSerializer(beers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from beers.models import Beer
from beers.permissions import IsBreweryOrReadOnly, IsBeerEditor
from beers.serializers import BeerSerializer


# class BeerList(generics.ListCreateAPIView):
#     queryset = Beer.objects.all()
#     serializer_class = BeerSerializer
#
#
# class BeerDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Beer.objects.all()
#     serializer_class = BeerSerializer

class BeerViewSet(viewsets.ModelViewSet):
    permission_classes = [IsBreweryOrReadOnly, IsAuthenticated]
    queryset = Beer.objects.all()
    serializer_class = BeerSerializer


class BeerByBreweryViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = BeerSerializer

    def get_queryset(self):
        return Beer.objects.filter(brewery=self.request.user)


class BeerEditorViewSet(viewsets.ModelViewSet):
    permission_classes = [IsBeerEditor]
    queryset = Beer.objects.all()
    serializer_class = BeerSerializer

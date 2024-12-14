from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BeerViewSet, BreweryViewSet

# Router for BeerViewSet
router = DefaultRouter()
router.register('beers', BeerViewSet, basename='beer')

# Manual paths for BreweryViewSet
brewery_urls = [
    path('', BreweryViewSet.as_view({'get': 'list_breweries'}), name='list-breweries'),
    path('count/', BreweryViewSet.as_view({'get': 'number_of_breweries'}), name='number-of-breweries'),
    path('<str:brewery_name>/beers/', BreweryViewSet.as_view({'get': 'get_beers_by_brewery'}), name='get-beers-by-brewery'),
]

# Manual path for get_beer_by_name
get_beer_by_name_url = [path('<str:beer_name>/', BeerViewSet.as_view({'get': 'get_beer_by_name'}), name='get-beer-by-name')]

urlpatterns = [
    path('', include(router.urls)),
    path('beers/name/', include((get_beer_by_name_url, 'beers'))),
    path('breweries/', include((brewery_urls, 'breweries'))),
]

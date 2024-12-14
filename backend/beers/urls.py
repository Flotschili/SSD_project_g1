from django.urls import path
from rest_framework.routers import SimpleRouter

from beers.views import BeerByBreweryViewSet, BeerViewSet

router = SimpleRouter()
router.register('by-brewery', BeerByBreweryViewSet, basename='beers-by-brewery')
router.register('', BeerViewSet, basename='beers')

urlpatterns = router.urls

from django.urls import path
from rest_framework.routers import SimpleRouter

from beers.views import BeerByBreweryViewSet, BeerEditorViewSet, BeerViewSet

router = SimpleRouter()
router.register('by-brewery', BeerByBreweryViewSet, basename='beers-by-brewery')
router.register('editor', BeerEditorViewSet, basename='beers-editor')
router.register('', BeerViewSet, basename='beers')

urlpatterns = router.urls

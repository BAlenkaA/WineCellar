from django.urls import path, include
from rest_framework import routers

from api.views import VineListRetrieveViewSet, CategoryRetriveViewSet

router = routers.SimpleRouter()

router.register(r'vine', VineListRetrieveViewSet)
router.register('categories', CategoryRetriveViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
from rest_framework import mixins, viewsets

from vine.models import Vine, Category
from api.serializers import VineSerializer
from api.permissions import AdminOrReadOnly


class VineListRetrieveViewSet(viewsets.ModelViewSet):
    queryset = Vine.objects.all()
    serializer_class = VineSerializer
    permission_classes = (AdminOrReadOnly,)


class CategoryRetriveViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Category.objects.all()

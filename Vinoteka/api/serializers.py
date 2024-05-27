from rest_framework import serializers

from vine.models import Vine


class VineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vine
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    pass

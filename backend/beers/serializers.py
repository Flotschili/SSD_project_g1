from rest_framework import serializers
from beers.models import Beer


class BeerSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name', 'description', 'brewery', 'created_at', 'updated_at')
        model = Beer

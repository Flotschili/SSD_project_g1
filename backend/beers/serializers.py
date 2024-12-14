from rest_framework import serializers
from beers.models import Beer


class BeerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Beer
        fields = [
            'id',
            'name',
            'brewery',
            'description',
            'alcohol_content',
            'beer_type',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


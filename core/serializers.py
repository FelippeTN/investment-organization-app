from rest_framework import serializers
from .models import Asset

class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = ['id', 'name', 'ticker', 'type', 'current_price', 'pl', 'pvp', 'dividend_yield']
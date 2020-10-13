from rest_framework import serializers

from .models import Coin, MarketCap


class CoinSerializer(serializers.ModelSerializer):
    """Class for Coin Serializer."""

    class Meta:
        """Nested Meta Class."""

        model = Coin
        fields = '__all__'


class MarketCapSerializer(serializers.ModelSerializer):
    """Class for MarketCap Serializer."""

    class Meta:
        """Nested Meta Class."""

        model = MarketCap
        fields = '__all__'
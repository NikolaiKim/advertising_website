from rest_framework import serializers

from advert.models import Advert


# Сериализатор для объявления
class AdvertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advert
        fields = ('price', 'title', 'description',)

from rest_framework import serializers

from advert.models import Advert


class AdvertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advert
        fields = ('price', 'title', 'description',)

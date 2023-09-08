from rest_framework import serializers

from feedback.models import Feedback


# Сериализатор для отзывов
class FeedbackSerializer(serializers.ModelSerializer):
    text = serializers.JSONField()

    class Meta:
        model = Feedback
        fields = ('text',)

from django.urls import path

from feedback.apps import FeedbackConfig
from feedback.views import FeedbackAPIView, FeedbackRetrieveAPIView

app_name = FeedbackConfig.name

urlpatterns = [
    path("api/ads/<int:advert_id>/comments/", FeedbackAPIView.as_view(), name='feedback'),
    path("api/ads/<int:advert_id>/comments/<int:pk>/", FeedbackRetrieveAPIView.as_view(), name='feedback_retrieve'),
]

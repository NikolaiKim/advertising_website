from django.urls import path

from advert.apps import AdvertConfig
from advert.views import UserAdvertListAPIView, AdvertAPIView, AdvertRetrieveAPI
from feedback.views import FeedbackAPIView, FeedbackRetrieveAPIView

app_name = AdvertConfig.name

# урлы для всех представлений объявлений и отзывов
urlpatterns = [
    path("api/ads/", AdvertAPIView.as_view(), name='adverts'),
    path("api/ads/me/", UserAdvertListAPIView.as_view(), name='user_adverts_list'),
    path("api/ads/<int:pk>/", AdvertRetrieveAPI.as_view(), name='advert_retrieve'),
    path("api/ads/<int:advert_id>/comments/", FeedbackAPIView.as_view(), name='feedback'),
    path("api/ads/<int:advert_id>/comments/<int:pk>/", FeedbackRetrieveAPIView.as_view(), name='feedback_retrieve'),
]

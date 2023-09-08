from django.urls import include, path, re_path
from djoser.views import UserViewSet
from rest_framework.routers import SimpleRouter

from user.apps import UserConfig
from user.views import ActivateUserEmail, AccessTokenView, CustomTokenRefreshView

app_name = UserConfig.name

users_router = SimpleRouter()

# обратите внимание, что здесь в роуте мы регистрируем ViewSet,
# который импортирован из приложения Djoser
users_router.register("users", UserViewSet, basename="users")

urlpatterns = [
    path("api/", include(users_router.urls)),

    re_path(r'^auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.jwt')),
    path('activate/<str:uid>/<str:token>/', ActivateUserEmail.as_view(), name='activate email'),
    path('api/refresh/', CustomTokenRefreshView.as_view(), name='refresh_token'),
    path('api/token/', AccessTokenView.as_view(), name='access_token'),
]

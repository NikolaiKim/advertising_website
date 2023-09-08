from django.urls import include, path, re_path
from djoser.views import UserViewSet
from rest_framework.routers import SimpleRouter

from user.apps import UserConfig
from user.views import (
    AccessTokenView, CustomTokenRefreshView,
    ActivateUserEmail)

app_name = UserConfig.name

users_router = SimpleRouter()

# Используем настройки для корректной работы Djoser
users_router.register("users", UserViewSet, basename="users")

# Урлы для отображений пользователя
urlpatterns = [
    path("api/", include(users_router.urls)),

    re_path(r'^auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.jwt')),
    path(
        'auth/users/activate/<str:uid>/<str:token>/',
        ActivateUserEmail.as_view(),
        name='user-activate'
    ),
    path(
        'api/refresh/',
        CustomTokenRefreshView.as_view(),
        name='refresh_token'
    ),
    path(
        'api/token/',
        AccessTokenView.as_view(),
        name='access_token'
    ),
]

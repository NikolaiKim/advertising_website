from django.urls import include, path, re_path
from djoser.views import UserViewSet
from rest_framework.routers import SimpleRouter

from user.apps import UserConfig
from user.views import ActivateUserEmail

app_name = UserConfig.name

users_router = SimpleRouter()

# обратите внимание, что здесь в роуте мы регистрируем ViewSet,
# который импортирован из приложения Djoser
users_router.register("users", UserViewSet, basename="users")

urlpatterns = [
    path("", include(users_router.urls)),

    re_path(r'^auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    path('activate/<str:uid>/<str:token>/', ActivateUserEmail.as_view(), name='activate email'),
]

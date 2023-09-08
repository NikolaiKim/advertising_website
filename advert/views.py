from django.http import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from advert.filters import AdvertFilter
from advert.models import Advert
from advert.paginators import AdvertPaginator
from advert.permissions import IsAdminOrOwner
from advert.serializers import AdvertSerializer


# Представления для объявлений
class AdvertAPIView(APIView):
    """Представление для списка объявлений с фильтрацией"""
    serializer_class = AdvertSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = AdvertFilter

    def get_permissions(self):
        """Ограничение для метода гет, которое разрешает всем просматривать список объявлений. В остальных случаях
        нужна аутентификация
        """
        method = self.request.method
        if method == 'GET':
            return [AllowAny()]
        else:
            return [IsAuthenticated()]

    def get(self, request):
        """Метод get, который отдает список объявлений постранично 4 шт. на страницу по дате создания
        от позднего к раннему"""
        adverts = Advert.objects.all().values().order_by('-created_at')
        paginator = PageNumberPagination()
        paginator.page_size = 4
        result_page = paginator.paginate_queryset(adverts, request)
        serializer = AdvertSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        """Метод post, который дает пользователю добавить новое объявление"""
        serializer = AdvertSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=self.request.user)
            return Response({'post': serializer.data})
        return JsonResponse(serializer.errors, status=400)


class UserAdvertListAPIView(generics.ListAPIView):
    """Представление для получения списка объявлений пользователя"""
    serializer_class = AdvertSerializer
    pagination_class = AdvertPaginator

    def get_queryset(self):
        """Функция получения объектов объявлений пользователя"""
        return Advert.objects.filter(author=self.request.user).order_by('-created_at')


class AdvertRetrieveAPI(APIView):
    """Представление для работы с выбранным объявлением, которое может иметь проверку ограничения объекта на создателя,
    либо админа
    """
    serializer_class = AdvertSerializer
    queryset = Advert.objects.all()
    permission_classes = (IsAdminOrOwner,)

    def get(self, request, pk):
        """Получение объявления по его pk"""
        advert = Advert.objects.get(pk=pk)
        serializer = AdvertSerializer(advert)
        return JsonResponse(serializer.data)

    def patch(self, request, *args, **kwargs):
        """Редактирование объявления с проверкой ограничения на создателя или админа"""
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({"error": "Method PUT not allowed"})

        try:
            instance = Advert.objects.get(pk=pk)
        except:
            return Response({"error": "Object does not exists"})

        serializer = AdvertSerializer(data=request.data, instance=instance)
        self.check_object_permissions(request, obj=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"post": serializer.data})

    def delete(self, request, *args, **kwargs):
        """Удаление объявления с проверкой ограничения на создателя или админа"""
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({"error": "Method DELETE not allowed"})
        advert = Advert.objects.get(pk=pk)
        self.check_object_permissions(request, obj=advert)
        advert.delete()
        return Response({"post": "delete post " + str(pk)})

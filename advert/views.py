from django.http import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.inspectors import SwaggerAutoSchema
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from advert import filters
from advert.models import Advert
from advert.paginators import AdvertPaginator
from advert.permissions import IsAdminOrOwner
from advert.serializers import AdvertSerializer


class OperationID(SwaggerAutoSchema):
    def get_operation_id(self, operation_keys):
        operation_id = super(OperationID, self).get_operation_id(operation_keys)
        if operation_id == "api_ads_me_list":
            return "Список объявлений пользователя"


# Представления для объявлений
class AdvertAPIView(APIView):
    """Представление для списка объявлений с фильтрацией"""
    serializer_class = AdvertSerializer
    queryset = Advert.objects.all()
    filter_backends = [DjangoFilterBackend, filters.AdvertFilter]
    search_fields = ["title", "description", ]

    def get_permissions(self):
        """Ограничение для метода гет,
        которое разрешает всем просматривать список объявлений.
        В остальных случаяхнужна аутентификация
        """
        method = self.request.method
        if method == 'GET':
            return [AllowAny()]
        else:
            return [IsAuthenticated()]

    @swagger_auto_schema(operation_id="Список объявлений")
    def get(self, request):
        """Метод get,
        который отдает список объявлений постранично
        4 шт. на страницу
        по дате создания от позднего к раннему"""
        filterurl = self.request.query_params.get('search', None)
        adverts = Advert.objects.all().values().order_by('-created_at')
        if filterurl is not None:
            adverts = Advert.objects.filter(title__icontains=filterurl)
        paginator = PageNumberPagination()
        paginator.page_size = 4
        result_page = paginator.paginate_queryset(adverts, request)
        serializer = AdvertSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    @swagger_auto_schema(operation_id="Добавить объявление")
    def post(self, request):
        """Метод post, который
        дает пользователю добавить новое объявление"""
        serializer = AdvertSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=self.request.user)
            return Response({'post': serializer.data})
        return JsonResponse(serializer.errors, status=400)


class UserAdvertListAPIView(generics.ListAPIView):
    """Представление для
    получения списка объявлений пользователя"""
    serializer_class = AdvertSerializer
    pagination_class = AdvertPaginator
    swagger_schema = OperationID

    def get_queryset(self):
        """Функция получения
        объектов объявлений пользователя"""
        return Advert.objects.filter(
            author=self.request.user
        ).order_by('-created_at')


class AdvertRetrieveAPI(APIView):
    """Представление для работы с выбранным объявлением,
    которое может иметь проверку ограничения объекта на создателя,
    либо админа
    """
    serializer_class = AdvertSerializer
    queryset = Advert.objects.all()
    permission_classes = (IsAdminOrOwner,)

    @swagger_auto_schema(operation_id="Получить объявление по его id")
    def get(self, request, pk):
        """Получение объявления по его pk"""
        advert = Advert.objects.get(pk=pk)
        serializer = AdvertSerializer(advert)
        return JsonResponse(serializer.data)

    @swagger_auto_schema(operation_id="Изменить объявление")
    def patch(self, request, *args, **kwargs):
        """Редактирование объявления с проверкой
        ограничения на создателя или админа"""
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({"error": "Method PUT not allowed"})

        try:
            instance = Advert.objects.get(pk=pk)
        except Exception:
            return Response({"error": "Object does not exists"})

        serializer = AdvertSerializer(data=request.data, instance=instance)
        self.check_object_permissions(request, obj=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"post": serializer.data})

    @swagger_auto_schema(operation_id="Удалить объявление")
    def delete(self, request, *args, **kwargs):
        """Удаление объявления с проверкой
        ограничения на создателя или админа"""
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({"error": "Method DELETE not allowed"})
        advert = Advert.objects.get(pk=pk)
        self.check_object_permissions(request, obj=advert)
        advert.delete()
        return Response({"post": "delete post " + str(pk)})

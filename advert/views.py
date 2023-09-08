from django.http import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from advert.filters import AdvertFilter
from advert.models import Advert
from advert.paginators import AdvertPaginator
from advert.serializers import AdvertSerializer


# Create your views here.
class AdvertAPIView(APIView):
    serializer_class = AdvertSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = AdvertFilter

    # permission_classes = [IsUser | IsModerator]

    def get(self, request):
        adverts = Advert.objects.all().values().order_by('-created_at')
        paginator = PageNumberPagination()
        paginator.page_size = 4
        result_page = paginator.paginate_queryset(adverts, request)
        serializer = AdvertSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        #Создание
        serializer = AdvertSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=self.request.user)
            return Response({'post': serializer.data})
        return JsonResponse(serializer.errors, status=400)


class UserAdvertListAPIView(generics.ListAPIView):
    '''Контролер для получения списка объявлений пользователя'''
    serializer_class = AdvertSerializer
    pagination_class = AdvertPaginator

    # permission_classes = [IsPublic | IsAuthenticated]

    def get_queryset(self):
        return Advert.objects.filter(author=self.request.user).order_by('-created_at')


class AdvertRetrieveAPI(APIView):
    serializer_class = AdvertSerializer
    queryset = Advert.objects.all()

    # permission_classes = [IsUser | IsModerator]

    def get(self, request, pk):
        advert = Advert.objects.get(pk=pk)
        serializer = AdvertSerializer(advert)
        return JsonResponse(serializer.data)

    def patch(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({"error": "Method PUT not allowed"})

        try:
            instance = Advert.objects.get(pk=pk)
        except:
            return Response({"error": "Object does not exists"})

        serializer = AdvertSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"post": serializer.data})

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({"error": "Method DELETE not allowed"})
        Advert.objects.filter(pk=pk).delete()
        return Response({"post": "delete post " + str(pk)})

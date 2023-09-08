from django.http import JsonResponse
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from advert.models import Advert
from feedback.models import Feedback
from feedback.permissions import IsAdminOrOwnerFeedback
from feedback.serializers import FeedbackSerializer


# Представления для отзывов.
class FeedbackAPIView(APIView):
    """Представление для списка отзывов"""
    serializer_class = FeedbackSerializer

    def get_permissions(self):
        """Ограничение на пользователей прошедших аутентификацию"""
        return [IsAuthenticated()]

    def get(self, request, advert_id):
        """Метод get, который возвращает список отзывов к объявлению по дате создания от позднего к раннему
        с пагинацией по 5 штук на страницу"""
        feedback = Feedback.objects.filter(advert_id=advert_id).values().order_by('-created_at')
        paginator = PageNumberPagination()
        paginator.page_size = 5
        result_page = paginator.paginate_queryset(feedback, request)
        serializer = FeedbackSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, advert_id):
        """Метод post, который позволяет авторизованному пользователю добавить отзыв"""
        serializer = FeedbackSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            serializer.save(user=self.request.user, advert=Advert.objects.get(pk=advert_id))
            return Response({'post': serializer.data})
        return JsonResponse(serializer.errors, status=400)


class FeedbackRetrieveAPIView(APIView):
    """Представление для отзыва с ограничением на админа или создателя"""
    serializer_class = FeedbackSerializer
    queryset = Feedback.objects.all()
    permission_classes = (IsAdminOrOwnerFeedback,)

    def get(self, request, advert_id, pk):
        """Метод get, который возвращает отзыв по pk"""
        feedback = Feedback.objects.filter(advert_id=advert_id).get(pk=pk)
        self.check_object_permissions(request, obj=feedback)
        serializer = FeedbackSerializer(feedback)
        return JsonResponse(serializer.data)

    def patch(self, request, *args, **kwargs):
        """Метод patch, который позволяет пользователю или администратору отредактировать отзыв"""
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({"error": "Method PUT not allowed"})

        try:
            instance = Feedback.objects.get(pk=pk)
        except:
            return Response({"error": "Object does not exists"})

        serializer = FeedbackSerializer(data=request.data, instance=instance)
        self.check_object_permissions(request, obj=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"post": serializer.data})

    def delete(self, request, *args, **kwargs):
        """Метод delete, который позволяет пользователю или администратору удалить отзыв"""
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({"error": "Method DELETE not allowed"})
        feedback = Feedback.objects.get(pk=pk)
        self.check_object_permissions(request, obj=feedback)
        feedback.delete()
        return Response({"post": "delete post " + str(pk)})

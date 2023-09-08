from django.http import JsonResponse
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from advert.models import Advert
from feedback.models import Feedback
from feedback.serializers import FeedbackSerializer


# Create your views here.
class FeedbackAPIView(APIView):
    serializer_class = FeedbackSerializer

    # permission_classes = [IsUser | IsModerator]

    def get(self, request, advert_id):
        feedback = Feedback.objects.filter(advert_id=advert_id).values().order_by('-created_at')
        paginator = PageNumberPagination()
        paginator.page_size = 5
        result_page = paginator.paginate_queryset(feedback, request)
        serializer = FeedbackSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, advert_id):
        serializer = FeedbackSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            serializer.save(user=self.request.user, advert=Advert.objects.get(pk=advert_id))
            return Response({'post': serializer.data})
        return JsonResponse(serializer.errors, status=400)


class FeedbackRetrieveAPIView(APIView):
    serializer_class = FeedbackSerializer
    queryset = Feedback.objects.all()

    # permission_classes = [IsUser | IsModerator]

    def get(self, request, advert_id, pk):
        feedback = Feedback.objects.filter(advert_id=advert_id).get(pk=pk)
        serializer = FeedbackSerializer(feedback)
        return JsonResponse(serializer.data)

    def patch(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({"error": "Method PUT not allowed"})

        try:
            instance = Feedback.objects.get(pk=pk)
        except:
            return Response({"error": "Object does not exists"})

        serializer = FeedbackSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"post": serializer.data})

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({"error": "Method DELETE not allowed"})
        Feedback.objects.filter(pk=pk).delete()
        return Response({"post": "delete post " + str(pk)})

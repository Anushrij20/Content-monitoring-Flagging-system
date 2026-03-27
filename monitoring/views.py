from django.shortcuts import render

# Create your views here.
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Keyword, Flag
from .serializers import KeywordSerializer, FlagSerializer, FlagStatusUpdateSerializer
from .services.scan import run_scan


class KeywordCreateView(generics.CreateAPIView):
    queryset = Keyword.objects.all()
    serializer_class = KeywordSerializer


class FlagListView(generics.ListAPIView):
    queryset = Flag.objects.filter(suppressed=False).select_related("keyword", "content_item")
    serializer_class = FlagSerializer


class ScanTriggerView(APIView):
    def post(self, request):
        stats = run_scan()
        return Response({
            "message": "Scan completed successfully",
            **stats
        }, status=status.HTTP_200_OK)


class FlagStatusUpdateView(generics.UpdateAPIView):
    queryset = Flag.objects.all()
    serializer_class = FlagStatusUpdateSerializer

    def patch(self, request, *args, **kwargs):
        flag = self.get_object()
        serializer = self.get_serializer(flag, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        new_status = serializer.validated_data["status"]
        flag.status = new_status

        if new_status == Flag.STATUS_IRRELEVANT:
            flag.suppressed = True
            flag.suppressed_at = timezone.now()
            flag.content_last_updated_at_review = flag.content_item.last_updated
            flag.reviewed_at = timezone.now()

        elif new_status == Flag.STATUS_RELEVANT:
            flag.suppressed = False
            flag.suppressed_at = None
            flag.reviewed_at = timezone.now()

        elif new_status == Flag.STATUS_PENDING:
            flag.suppressed = False
            flag.suppressed_at = None

        flag.save()

        return Response(FlagSerializer(flag).data, status=status.HTTP_200_OK)

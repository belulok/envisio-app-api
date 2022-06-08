"""
Views for the report APIs
"""
from rest_framework import (
    viewsets,
    status,
)

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Report
from report import serializers


class ReportViewSet(viewsets.ModelViewSet):
    """View for manage report APIs."""
    serializer_class = serializers.ReportDetailSerializer
    queryset = Report.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve reports for authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'list':
            return serializers.ReportSerializer
        elif self.action == 'upload_image':
            return serializers.ReportImageSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new report."""
        serializer.save(user=self.request.user)

    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """Upload an image to report"""
        report = self.get_object()
        serializer = self.get_serializer(report, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

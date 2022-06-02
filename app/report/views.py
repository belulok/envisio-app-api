"""
Views for the report APIs
"""
from rest_framework import (
    viewsets,
    mixins,
)
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import (
    Report,
    Job,
)
from report import serializers


class ReportViewSet(viewsets.ModelViewSet):
    """View for manage report APIs."""
    serializer_class = serializers.ReportSerializer
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

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new report."""
        serializer.save(user=self.request.user)


class JobViewSet(mixins.DestroyModelMixin,
                 mixins.UpdateModelMixin,
                 mixins.ListModelMixin,
                 viewsets.GenericViewSet):
    """Manage jobids in the database."""
    serializer_class = serializers.JobSerializer
    queryset = Job.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter queryset to authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-name')

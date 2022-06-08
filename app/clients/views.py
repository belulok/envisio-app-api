"""
Views for the clients APIs
"""
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Clients
from clients import serializers


class ClientsViewSet(viewsets.ModelViewSet):
    """View for manage client APIs"""
    serializer_class = serializers.ClientsDetailSerializer
    queryset = Clients.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrive clients for authenticated user"""
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):
        """Return the serializer class for request"""
        if self.action == 'list':
            return serializers.ClientsSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new client"""
        serializer.save(user=self.request.user)

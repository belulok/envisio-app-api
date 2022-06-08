"""
Serializers for clients APIs
"""
from rest_framework import serializers

from core.models import Clients


class ClientsSerializer(serializers.ModelSerializer):
    """Serializer for clients"""

    class Meta:
        model = Clients
        fields = ['id', 'name', 'location', 'logo']
        read_only_fields = ['id']


class ClientsDetailSerializer(ClientsSerializer):
    """Serializer for the client detail view"""

    class Meta(ClientsSerializer.Meta):
        fields = ClientsSerializer.Meta.fields + ['location']

"""Test for client API"""
from unittest import defaultTestLoader
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Clients

from clients.serializers import ClientsSerializer

CLIENTS_URL = reverse('client:client-list')

def create_clients(user, **params):
    """Create and return a sample client"""
    defaults = {
        'name':'Shell',
        'location':'Miri',
        'logo':'asdasas',
    }
    defaults.update(params)

    clients = Clients.objects.create(user=user, **defaults)
    return clients

class PublicClientsAPITests(TestCase):
    """Test unathenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API"""
        res = self.client.get(CLIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateClientsAPITests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create.user(
            'user@example.com',
            'testpass123',
        )
        self.client.force_authenticate(self.user)

    def test_retrive_clients(self):
        """Test retrieving a list of clients"""
        create_clients(user=self.user)
        create_clients(user=self.user)

        res = self.client.get(CLIENTS_URL)

        clients = Clients.objects.all().order_by('-id')
        serializer = ClientsSerializer(clients, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_clients_list_limited_to_user(self):
        """Test list of clients is limited to authenticate user"""
        other_user = get_user_model().objects.create_user(
            'other@example.com',
            'password123',
        )
        create_clients(user=other_user)
        create_clients(user=self.user)

        res = self.client.get(CLIENTS_URL)

        clients = Clients.objects.filter(user=self.user)
        serializer = ClientsSerializer(clients, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_0K)
        self.assertEqual(res.data, serializer.data)

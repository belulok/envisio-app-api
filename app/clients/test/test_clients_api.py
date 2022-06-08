"""Test for client API"""
# from unittest import defaultTestLoader
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


from rest_framework import status
from rest_framework.test import APIClient

from core.models import Clients

from clients.serializers import (
    ClientsSerializer,
    ClientsDetailSerializer,
    )

CLIENTS_URL = reverse('clients:clients-list')


def detail_url(clients_id):
    """Create and return a client detail URL"""
    return reverse('clients:clients-detail', args=[clients_id])


def create_clients(user, **params):
    """Create and return a sample client"""
    defaults = {
        'name': 'Shell',
        'location': 'Miri',
        'logo': 'asdasas',
    }
    defaults.update(params)

    clients = Clients.objects.create(user=user, **defaults)
    return clients


def create_user(**params):
    """Create and return a new user"""
    return get_user_model().objects.create_user(**params)


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
        self.user = create_user(email='user@example.com', password='test123')
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
        other_user = create_user(email='other@example.com', password='pass123')
        create_clients(user=other_user)
        create_clients(user=self.user)

        res = self.client.get(CLIENTS_URL)

        clients = Clients.objects.filter(user=self.user)
        serializer = ClientsSerializer(clients, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_clients_detail(self):
        """Test get client detail"""
        clients = create_clients(user=self.user)

        url = detail_url(clients.id)
        res = self.client.get(url)

        serializer = ClientsDetailSerializer(clients)
        self.assertEqual(res.data, serializer.data)

    def test_create_clients(self):
        """Test creating a clients"""
        payload = {
            'name': 'Shell',
            'location': 'Miri',
            'logo': 'asdasas',
        }
        res = self.client.post(CLIENTS_URL, payload)  # /api/clients/client

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        clients = Clients.objects.get(id=res.data['id'])
        for k, v in payload.items():
            self.assertEqual(getattr(clients, k), v)
        self.assertEqual(clients.user, self.user)

    def test_partial_update(self):
        """Test partial update of a client"""
        original_location = 'Miri'
        clients = create_clients(
            user=self.user,
            name='Shell',
            location=original_location,
            logo='asdasas',
        )

        payload = {'name': 'Shell'}
        url = detail_url(clients.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        clients.refresh_from_db()
        self.assertEqual(clients.name, payload['name'])
        self.assertEqual(clients.location, original_location)
        self.assertEqual(clients.user, self.user)

    def test_full_update(self):
        """Test full update of clients"""
        clients = create_clients(
            user=self.user,
            name='Shell',
            location='Miri',
            logo='asdasas',
        )

        payload = {
            'name': 'Shell',
            'location': 'Miri',
            'logo': 'asdasas',
        }
        url = detail_url(clients.id)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        clients.refresh_from_db()
        for k, v in payload.items():
            self.assertEqual(getattr(clients, k), v)
        self.assertEqual(clients.user, self.user)

    def test_update_user_returns_error(self):
        """"Test changing the recipe user results in an error."""
        new_user = create_user(email='user2@example.com', password="test123")
        clients = create_clients(user=self.user)

        payload = {'user': new_user.id}
        url = detail_url(clients.id)
        self.client.patch(url, payload)

        clients.refresh_from_db()
        self.assertEqual(clients.user, self.user)

    def test_delete_client(self):
        """Test deleting a client successful"""
        clients = create_clients(user=self.user)

        url = detail_url(clients.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Clients.objects.filter(id=clients.id).exists())

    def test_clients_other_users_clients_error(self):
        """Test trying to delete another users clients gives error"""
        new_user = create_user(email='user2@example.com', password='test123')
        clients = create_clients(user=new_user)

        url = detail_url(clients.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Clients.objects.filter(id=clients.id).exists())

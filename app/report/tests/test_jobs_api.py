"""
Tests for the job_id API.
"""
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Job

from report.serializers import JobSerializer


JOBS_URL = reverse('report:job-list')


def detail_url(job_id):
    """Create and return a job_id detail url."""
    return reverse('report:job-detail', args=[job_id])


def create_user(email='user@example.com', password='testpass123'):
    """Create and return a user."""
    return get_user_model().objects.create_user(email=email, password=password)


class PublicJobsApiTests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required for retrieving jobs."""
        res = self.client.get(JOBS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateJobsApiTests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_jobs(self):
        """Test retrieving a list of jobs."""
        Job.objects.create(user=self.user, name='JobId1')
        Job.objects.create(user=self.user, name='JobId2')

        res = self.client.get(JOBS_URL)

        jobs = Job.objects.all().order_by('-name')
        serializer = JobSerializer(jobs, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_jobs_limited_to_user(self):
        """Test list of jobIds is limited to authenticated user."""
        user2 = create_user(email='user2@example.com')
        Job.objects.create(user=user2, name='JobId1')
        job = Job.objects.create(user=self.user, name='JobId1')

        res = self.client.get(JOBS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], job.name)
        self.assertEqual(res.data[0]['id'], job.id)

    def test_update_jobid(self):
        """Test updating a jobid."""
        job = Job.objects.create(user=self.user, name='After Dinner')
        payload = {'name': 'Dessert'}
        url = detail_url(job.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        job.refresh_from_db()
        self.assertEqual(job.name, payload['name'])

    def test_delete_jobid(self):
        """Test deleting a jobid."""
        job = Job.objects.create(user=self.user, name='Breakfast')

        url = detail_url(job.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        job = Job.objects.filter(user=self.user)
        self.assertFalse(job.exists())

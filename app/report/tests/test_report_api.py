"""
Tests for report APIs.
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Report

from report.serializers import ReportSerializer


REPORTS_URL = reverse('report:report-list')


def create_report(user, **params):
    """Create and return a sample report."""
    defaults = {
        'job_id': 'abcde',
        'clients': 'abcde',
        'client_logo': 'abcde',
        'location': 'abcde',
    }
    defaults.update(params)

    report = Report.objects.create(user=user, **defaults)
    return report


class PublicReportAPITests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API."""
        res = self.client.get(REPORTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateReportApiTests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'user@example.com',
            'testpass123',
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_reports(self):
        """Test retrieving a list of reports."""
        create_report(user=self.user)
        create_report(user=self.user)

        res = self.client.get(REPORTS_URL)

        reports = Report.objects.all().order_by('-id')
        serializer = ReportSerializer(reports, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_report_list_limited_to_user(self):
        """Test list of reports is limited to authenticated user."""
        other_user = get_user_model().objects.create_user(
            'other@example.com',
            'password123',
        )
        create_report(user=other_user)
        create_report(user=self.user)

        res = self.client.get(REPORTS_URL)

        reports = Report.objects.filter(user=self.user)
        serializer = ReportSerializer(reports, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

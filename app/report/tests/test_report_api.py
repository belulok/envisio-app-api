"""
Tests for report APIs.
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Report

from report.serializers import (
    ReportSerializer,
    ReportDetailSerializer,
)


REPORTS_URL = reverse('report:report-list')


def detail_url(report_id):
    """Create and return a report detail URL."""
    return reverse('report:report-detail', args=[report_id])


def create_report(user, **params):
    """Create and return a sample report."""
    defaults = {
        'job_id': 'abcde',
        'description': 'abcde',
        'clients': 'abcde',
        'client_logo': 'abcde',
        'location': 'abcde',
    }
    defaults.update(params)

    report = Report.objects.create(user=user, **defaults)
    return report


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


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
        self.user = create_user(email='user@example.com', password='test123')
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
        other_user = create_user(email='other@example.com', password='test123')
        create_report(user=other_user)
        create_report(user=self.user)

        res = self.client.get(REPORTS_URL)

        reports = Report.objects.filter(user=self.user)
        serializer = ReportSerializer(reports, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_report_detail(self):
        """Test get report detail."""
        report = create_report(user=self.user)

        url = detail_url(report.id)
        res = self.client.get(url)

        serializer = ReportDetailSerializer(report)
        self.assertEqual(res.data, serializer.data)

    def test_create_report(self):
        """Test creating a report."""
        payload = {
            'job_id': 'abcde',
            'description': 'abcde',
            'clients': 'abcde',
            'client_logo': 'abcde',
            'location': 'abcde',
        }
        res = self.client.post(REPORTS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        report = Report.objects.get(id=res.data['id'])
        for k, v in payload.items():
            self.assertEqual(getattr(report, k), v)
        self.assertEqual(report.user, self.user)

    def test_partial_update(self):
        """Test partial update of a report."""
        original_location = 'https://example.com/report.pdf'
        report = create_report(
            user=self.user,
            job_id='Sample report title',
            location=original_location,
        )

        payload = {'job_id': 'New report title'}
        url = detail_url(report.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        report.refresh_from_db()
        self.assertEqual(report.job_id, payload['job_id'])
        self.assertEqual(report.location, original_location)
        self.assertEqual(report.user, self.user)

    def test_full_update(self):
        """Test full update of report."""
        report = create_report(
            user=self.user,
            job_id='Sample report title',
            location='https://exmaple.com/report.pdf',
            client_logo='Sample report description.',
        )

        payload = {
            'job_id': 'abcde',
            'description': 'abcde',
            'clients': 'abcde',
            'client_logo': 'abcde',
            'location': 'abcde',
        }
        url = detail_url(report.id)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        report.refresh_from_db()
        for k, v in payload.items():
            self.assertEqual(getattr(report, k), v)
        self.assertEqual(report.user, self.user)

    def test_update_user_returns_error(self):
        """Test changing the report user results in an error."""
        new_user = create_user(email='user2@example.com', password='test123')
        report = create_report(user=self.user)

        payload = {'user': new_user.id}
        url = detail_url(report.id)
        self.client.patch(url, payload)

        report.refresh_from_db()
        self.assertEqual(report.user, self.user)

    def test_delete_report(self):
        """Test deleting a report successful."""
        report = create_report(user=self.user)

        url = detail_url(report.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Report.objects.filter(id=report.id).exists())

    def test_report_other_users_report_error(self):
        """Test trying to delete another users report gives error."""
        new_user = create_user(email='user2@example.com', password='test123')
        report = create_report(user=new_user)

        url = detail_url(report.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Report.objects.filter(id=report.id).exists())

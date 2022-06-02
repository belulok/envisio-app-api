"""
Tests for report APIs.
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import (
    Report,
    Job,
)

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
        'clients': 'abcde',
        'client_logo': 'abcde',
        'location': 'abcde',
        'year': 'abcde',
        'month': 'abcde',
        'initial': 'abcde',
        'po_num': 'abcde',
        'hub': 'abcde',
        'platform_location': 'abcde',
        'survey_date': 'abcde',
        'inspection_by': 'abcde',
        'valve_tag_no': 'abcde',
        'valve_description': 'abcde',
        'valve_type': 'abcde',
        'functions': 'abcde',
        'valve_size': 'abcde',
        'valve_make': 'abcde',
        'actuator_make': 'abcde',
        'valve_photo': 'abcde',
        'p_and_id_no': 'abcde',
        'mal_sof': 'abcde',
        'mal_sof_others': 'abcde',
        'mal': 'abcde',
        'mal_warn': 'abcde',
        'fluid_type': 'abcde',
        'presure_upstream': 'abcde',
        'pressure_downstream': 'abcde',
        'flow_direction': 'abcde',
        'u3': 'abcde',
        'u2': 'abcde',
        'u1': 'abcde',
        'va': 'abcde',
        'vb': 'abcde',
        'vc': 'abcde',
        'vd': 'abcde',
        'd1': 'abcde',
        'd2': 'abcde',
        'd3': 'abcde',
        'result': 'abcde',
        'estimated_leak_rate': 'abcde',
        'color_code': 'abcde',
        'reason_not_tested': 'abcde',
        'discussion_result': 'abcde',
        'recommended_action': 'abcde',
        'maintenance_his': 'abcde',
        'avail_nameplate_tagno': 'abcde',
        'presence_downstream': 'abcde',
        'leak_visibility_body': 'abcde',
        'severe_corrosion_flanges': 'abcde',
        'visibility_crack_nuts_bolt': 'abcde',
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
            'clients': 'abcde',
            'client_logo': 'abcde',
            'location': 'abcde',
            'year': 'abcde',
            'month': 'abcde',
            'initial': 'abcde',
            'po_num': 'abcde',
            'hub': 'abcde',
            'platform_location': 'abcde',
            'survey_date': 'abcde',
            'inspection_by': 'abcde',
            'valve_tag_no': 'abcde',
            'valve_description': 'abcde',
            'valve_type': 'abcde',
            'functions': 'abcde',
            'valve_size': 'abcde',
            'valve_make': 'abcde',
            'actuator_make': 'abcde',
            'valve_photo': 'abcde',
            'p_and_id_no': 'abcde',
            'mal_sof': 'abcde',
            'mal_sof_others': 'abcde',
            'mal': 'abcde',
            'mal_warn': 'abcde',
            'fluid_type': 'abcde',
            'presure_upstream': 'abcde',
            'pressure_downstream': 'abcde',
            'flow_direction': 'abcde',
            'u3': 'abcde',
            'u2': 'abcde',
            'u1': 'abcde',
            'va': 'abcde',
            'vb': 'abcde',
            'vc': 'abcde',
            'vd': 'abcde',
            'd1': 'abcde',
            'd2': 'abcde',
            'd3': 'abcde',
            'result': 'abcde',
            'estimated_leak_rate': 'abcde',
            'color_code': 'abcde',
            'reason_not_tested': 'abcde',
            'discussion_result': 'abcde',
            'recommended_action': 'abcde',
            'maintenance_his': 'abcde',
            'avail_nameplate_tagno': 'abcde',
            'presence_downstream': 'abcde',
            'leak_visibility_body': 'abcde',
            'severe_corrosion_flanges': 'abcde',
            'visibility_crack_nuts_bolt': 'abcde',
        }
        res = self.client.post(REPORTS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        report = Report.objects.get(id=res.data['id'])
        for k, v in payload.items():
            self.assertEqual(getattr(report, k), v)
        self.assertEqual(report.user, self.user)

    def test_partial_update(self):
        """Test partial update of a report."""
        original_client = 'abcde'
        report = create_report(
            user=self.user,
            job_id='abcde',
            clients=original_client,
        )

        payload = {'job_id': 'abcde'}
        url = detail_url(report.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        report.refresh_from_db()
        self.assertEqual(report.job_id, payload['job_id'])
        self.assertEqual(report.clients, original_client)
        self.assertEqual(report.user, self.user)

    def test_full_update(self):
        """Test full update of report."""
        report = create_report(
            user=self.user,
            job_id='abcde',
            clients='abcde',
        )

        payload = {
            'job_id': 'abcde',
            'clients': 'abcde',
            'client_logo': 'abcde',
            'location': 'abcde',
            'year': 'abcde',
            'month': 'abcde',
            'initial': 'abcde',
            'po_num': 'abcde',
            'hub': 'abcde',
            'platform_location': 'abcde',
            'survey_date': 'abcde',
            'inspection_by': 'abcde',
            'valve_tag_no': 'abcde',
            'valve_description': 'abcde',
            'valve_type': 'abcde',
            'functions': 'abcde',
            'valve_size': 'abcde',
            'valve_make': 'abcde',
            'actuator_make': 'abcde',
            'valve_photo': 'abcde',
            'p_and_id_no': 'abcde',
            'mal_sof': 'abcde',
            'mal_sof_others': 'abcde',
            'mal': 'abcde',
            'mal_warn': 'abcde',
            'fluid_type': 'abcde',
            'presure_upstream': 'abcde',
            'pressure_downstream': 'abcde',
            'flow_direction': 'abcde',
            'u3': 'abcde',
            'u2': 'abcde',
            'u1': 'abcde',
            'va': 'abcde',
            'vb': 'abcde',
            'vc': 'abcde',
            'vd': 'abcde',
            'd1': 'abcde',
            'd2': 'abcde',
            'd3': 'abcde',
            'result': 'abcde',
            'estimated_leak_rate': 'abcde',
            'color_code': 'abcde',
            'reason_not_tested': 'abcde',
            'discussion_result': 'abcde',
            'recommended_action': 'abcde',
            'maintenance_his': 'abcde',
            'avail_nameplate_tagno': 'abcde',
            'presence_downstream': 'abcde',
            'leak_visibility_body': 'abcde',
            'severe_corrosion_flanges': 'abcde',
            'visibility_crack_nuts_bolt': 'abcde',
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

    def test_create_report_with_new_jobs(self):
        """Test creating a report with new jobid."""
        payload = {
            'job_id': 'abcde',
            'clients': 'abcde',
            'client_logo': 'abcde',
            'location': 'abcde',
            'year': 'abcde',
            'month': 'abcde',
            'initial': 'abcde',
            'po_num': 'abcde',
            'hub': 'abcde',
            'platform_location': 'abcde',
            'survey_date': 'abcde',
            'inspection_by': 'abcde',
            'valve_tag_no': 'abcde',
            'valve_description': 'abcde',
            'valve_type': 'abcde',
            'functions': 'abcde',
            'valve_size': 'abcde',
            'valve_make': 'abcde',
            'actuator_make': 'abcde',
            'valve_photo': 'abcde',
            'p_and_id_no': 'abcde',
            'mal_sof': 'abcde',
            'mal_sof_others': 'abcde',
            'mal': 'abcde',
            'mal_warn': 'abcde',
            'fluid_type': 'abcde',
            'presure_upstream': 'abcde',
            'pressure_downstream': 'abcde',
            'flow_direction': 'abcde',
            'u3': 'abcde',
            'u2': 'abcde',
            'u1': 'abcde',
            'va': 'abcde',
            'vb': 'abcde',
            'vc': 'abcde',
            'vd': 'abcde',
            'd1': 'abcde',
            'd2': 'abcde',
            'd3': 'abcde',
            'result': 'abcde',
            'estimated_leak_rate': 'abcde',
            'color_code': 'abcde',
            'reason_not_tested': 'abcde',
            'discussion_result': 'abcde',
            'recommended_action': 'abcde',
            'maintenance_his': 'abcde',
            'avail_nameplate_tagno': 'abcde',
            'presence_downstream': 'abcde',
            'leak_visibility_body': 'abcde',
            'severe_corrosion_flanges': 'abcde',
            'visibility_crack_nuts_bolt': 'abcde',
            'jobs': [{'name': 'Thai'}, {'name': 'Dinner'}],
        }
        res = self.client.post(REPORTS_URL, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        reports = Report.objects.filter(user=self.user)
        self.assertEqual(reports.count(), 1)
        report = reports[0]
        self.assertEqual(report.jobs.count(), 2)
        for job in payload['jobs']:
            exists = report.jobs.filter(
                name=job['name'],
                user=self.user,
            ).exists()
            self.assertTrue(exists)

    def test_create_report_with_existing_jobs(self):
        """Test creating a report with existing jobid."""
        job_1234 = Job.objects.create(user=self.user, name='Indian')
        payload = {
            'job_id': 'abcde',
            'clients': 'abcde',
            'client_logo': 'abcde',
            'location': 'abcde',
            'year': 'abcde',
            'month': 'abcde',
            'initial': 'abcde',
            'po_num': 'abcde',
            'hub': 'abcde',
            'platform_location': 'abcde',
            'survey_date': 'abcde',
            'inspection_by': 'abcde',
            'valve_tag_no': 'abcde',
            'valve_description': 'abcde',
            'valve_type': 'abcde',
            'functions': 'abcde',
            'valve_size': 'abcde',
            'valve_make': 'abcde',
            'actuator_make': 'abcde',
            'valve_photo': 'abcde',
            'p_and_id_no': 'abcde',
            'mal_sof': 'abcde',
            'mal_sof_others': 'abcde',
            'mal': 'abcde',
            'mal_warn': 'abcde',
            'fluid_type': 'abcde',
            'presure_upstream': 'abcde',
            'pressure_downstream': 'abcde',
            'flow_direction': 'abcde',
            'u3': 'abcde',
            'u2': 'abcde',
            'u1': 'abcde',
            'va': 'abcde',
            'vb': 'abcde',
            'vc': 'abcde',
            'vd': 'abcde',
            'd1': 'abcde',
            'd2': 'abcde',
            'd3': 'abcde',
            'result': 'abcde',
            'estimated_leak_rate': 'abcde',
            'color_code': 'abcde',
            'reason_not_tested': 'abcde',
            'discussion_result': 'abcde',
            'recommended_action': 'abcde',
            'maintenance_his': 'abcde',
            'avail_nameplate_tagno': 'abcde',
            'presence_downstream': 'abcde',
            'leak_visibility_body': 'abcde',
            'severe_corrosion_flanges': 'abcde',
            'visibility_crack_nuts_bolt': 'abcde',
            'jobs': [{'name': 'Indian'}, {'name': 'Breakfast'}],
        }
        res = self.client.post(REPORTS_URL, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        reports = Report.objects.filter(user=self.user)
        self.assertEqual(reports.count(), 1)
        report = reports[0]
        self.assertEqual(report.jobs.count(), 2)
        self.assertIn(job_1234, report.jobs.all())
        for job in payload['jobs']:
            exists = report.jobs.filter(
                name=job['name'],
                user=self.user,
            ).exists()
            self.assertTrue(exists)

    def test_create_job_on_update(self):
        """Test create job when updating a report."""
        report = create_report(user=self.user)

        payload = {'jobs': [{'name': 'Lunch'}]}
        url = detail_url(report.id)
        res = self.client.patch(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        new_job = Job.objects.get(user=self.user, name='Lunch')
        self.assertIn(new_job, report.jobs.all())

    def test_update_report_assign_job(self):
        """Test assigning an existing tag when updating a report."""
        job_breakfast = Job.objects.create(user=self.user, name='Breakfast')
        report = create_report(user=self.user)
        report.jobs.add(job_breakfast)

        job_lunch = Job.objects.create(user=self.user, name='Lunch')
        payload = {'jobs': [{'name': 'Lunch'}]}
        url = detail_url(report.id)
        res = self.client.patch(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn(job_lunch, report.jobs.all())
        self.assertNotIn(job_breakfast, report.jobs.all())

    def test_clear_report_jobs(self):
        """Test clearing a report jobs."""
        job = Job.objects.create(user=self.user, name='Dessert')
        report = create_report(user=self.user)
        report.jobs.add(job)

        payload = {'jobs': []}
        url = detail_url(report.id)
        res = self.client.patch(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(report.jobs.count(), 0)

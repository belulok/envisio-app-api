"""
Tests for models.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


class ModelTests(TestCase):
    """Test models."""

    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successful."""
        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email is normalized for new users."""
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.com', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'sample123')
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Test that creating a user without an email raises a ValueError."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'test123')

    def test_create_superuser(self):
        """Test creating a superuser."""
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'test123',
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_report(self):
        """Test creating a report is successful."""
        user = get_user_model().objects.create_user(
            'test@example.com',
            'testpass123',
        )
        report = models.Report.objects.create(
            user=user,
            job_id='abcde',
            clients='abcde',
            client_logo='abcde',
            location='abcde',
            year='abcde',
            month='abcde',
            initial='abcde',
            po_num='abcde',
            hub='abcde',
            platform_location='abcde',
            survey_date='abcde',
            inspection_by='abcde',
            valve_tag_no='abcde',
            valve_description='abcde',
            valve_type='abcde',
            functions='abcde',
            valve_size='abcde',
            valve_make='abcde',
            actuator_make='abcde',
            valve_photo='abcde',
            p_and_id_no='abcde',
            mal_sof='abcde',
            mal_sof_others='abcde',
            mal='abcde',
            mal_warn='abcde',
            fluid_type='abcde',
            presure_upstream='abcde',
            pressure_downstream='abcde',
            flow_direction='abcde',
            u3='abcde',
            u2='abcde',
            u1='abcde',
            va='abcde',
            vb='abcde',
            vc='abcde',
            vd='abcde',
            d1='abcde',
            d2='abcde',
            d3='abcde',
            result='abcde',
            estimated_leak_rate='abcde',
            color_code='abcde',
            reason_not_tested='abcde',
            discussion_result='abcde',
            recommended_action='abcde',
            maintenance_his='abcde',
            avail_nameplate_tagno='abcde',
            presence_downstream='abcde',
            leak_visibility_body='abcde',
            severe_corrosion_flanges='abcde',
            visibility_crack_nuts_bolt='abcde',
        )

        self.assertEqual(str(report), report.job_id)

    def test_create_clients(self):
        """Test creating a client is successful"""
        user = get_user_model().objects.create_user(
            'test@example.com',
            'testpass123',
        )
        clients = models.Clients.objects.create(
            user=user,
            name='Shell',
            location='Miri',
            logo='asdsa',
        )

        self.assertEqual(str(clients), clients.name)
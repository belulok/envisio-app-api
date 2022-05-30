"""
Database models.
"""
from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

# Create your models here.


class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""
        if not email:
            raise ValueError('User must have an email address.')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and return a new superuser."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Report(models.Model):
    """Report object."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    job_id = models.CharField(max_length=200)
    clients = models.CharField(max_length=200)
    client_logo = models.CharField(max_length=200)
    # client_logo = models.ImageField(upload_to='images/')
    location = models.CharField(max_length=200)
    year = models.CharField(max_length=200)
    month = models.CharField(max_length=200)
    initial = models.CharField(max_length=200)
    po_num = models.CharField(max_length=200)
    hub = models.CharField(max_length=200)
    platform_location = models.CharField(max_length=200)
    survey_date = models.CharField(max_length=200)
    inspection_by = models.CharField(max_length=200)

    # valve specification & information
    valve_tag_no = models.CharField(max_length=200)
    valve_description = models.CharField(max_length=200)
    valve_type = models.CharField(max_length=200)
    functions = models.CharField(max_length=200)
    valve_size = models.CharField(max_length=200)
    valve_make = models.CharField(max_length=200)
    actuator_make = models.CharField(max_length=200)
    valve_photo = models.CharField(max_length=200)
    # valve_photo = models.ImageField(upload_to='images/')
    p_and_id_no = models.CharField(max_length=200)
    mal_sof = models.CharField(max_length=200)
    mal_sof_others = models.CharField(max_length=200)
    mal = models.CharField(max_length=200)
    mal_warn = models.CharField(max_length=200)

    # AE Test Condition
    fluid_type = models.CharField(max_length=200)
    presure_upstream = models.CharField(max_length=200)
    pressure_downstream = models.CharField(max_length=200)
    flow_direction = models.CharField(max_length=200)

    # result & discussion
    u3 = models.CharField(max_length=200)
    u2 = models.CharField(max_length=200)
    u1 = models.CharField(max_length=200)
    va = models.CharField(max_length=200)
    vb = models.CharField(max_length=200)
    vc = models.CharField(max_length=200)
    vd = models.CharField(max_length=200)
    d1 = models.CharField(max_length=200)
    d2 = models.CharField(max_length=200)
    d3 = models.CharField(max_length=200)

    result = models.CharField(max_length=200)
    estimated_leak_rate = models.CharField(max_length=200)
    color_code = models.CharField(max_length=200)
    reason_not_tested = models.CharField(max_length=200)
    discussion_result = models.CharField(max_length=200)
    recommended_action = models.CharField(max_length=200)
    maintenance_his = models.CharField(max_length=200)

    # vale external condition assessment
    avail_nameplate_tagno = models.CharField(max_length=200)
    presence_downstream = models.CharField(max_length=200)
    leak_visibility_body = models.CharField(max_length=200)
    severe_corrosion_flanges = models.CharField(max_length=200)
    visibility_crack_nuts_bolt = models.CharField(max_length=200)

    def __str__(self):
        return self.job_id

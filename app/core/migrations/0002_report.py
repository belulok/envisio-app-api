# Generated by Django 3.2.13 on 2022-05-30 05:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_id', models.CharField(max_length=200)),
                ('clients', models.CharField(max_length=200)),
                ('client_logo', models.CharField(max_length=200)),
                ('location', models.CharField(max_length=200)),
                ('year', models.CharField(max_length=200)),
                ('month', models.CharField(max_length=200)),
                ('initial', models.CharField(max_length=200)),
                ('po_num', models.CharField(max_length=200)),
                ('hub', models.CharField(max_length=200)),
                ('platform_location', models.CharField(max_length=200)),
                ('survey_date', models.CharField(max_length=200)),
                ('inspection_by', models.CharField(max_length=200)),
                ('valve_tag_no', models.CharField(max_length=200)),
                ('valve_description', models.CharField(max_length=200)),
                ('valve_type', models.CharField(max_length=200)),
                ('functions', models.CharField(max_length=200)),
                ('valve_size', models.CharField(max_length=200)),
                ('valve_make', models.CharField(max_length=200)),
                ('actuator_make', models.CharField(max_length=200)),
                ('valve_photo', models.CharField(max_length=200)),
                ('p_and_id_no', models.CharField(max_length=200)),
                ('mal_sof', models.CharField(max_length=200)),
                ('mal_sof_others', models.CharField(max_length=200)),
                ('mal', models.CharField(max_length=200)),
                ('mal_warn', models.CharField(max_length=200)),
                ('fluid_type', models.CharField(max_length=200)),
                ('presure_upstream', models.CharField(max_length=200)),
                ('pressure_downstream', models.CharField(max_length=200)),
                ('flow_direction', models.CharField(max_length=200)),
                ('u3', models.CharField(max_length=200)),
                ('u2', models.CharField(max_length=200)),
                ('u1', models.CharField(max_length=200)),
                ('va', models.CharField(max_length=200)),
                ('vb', models.CharField(max_length=200)),
                ('vc', models.CharField(max_length=200)),
                ('vd', models.CharField(max_length=200)),
                ('d1', models.CharField(max_length=200)),
                ('d2', models.CharField(max_length=200)),
                ('d3', models.CharField(max_length=200)),
                ('result', models.CharField(max_length=200)),
                ('estimated_leak_rate', models.CharField(max_length=200)),
                ('color_code', models.CharField(max_length=200)),
                ('reason_not_tested', models.CharField(max_length=200)),
                ('discussion_result', models.CharField(max_length=200)),
                ('recommended_action', models.CharField(max_length=200)),
                ('maintenance_his', models.CharField(max_length=200)),
                ('avail_nameplate_tagno', models.CharField(max_length=200)),
                ('presence_downstream', models.CharField(max_length=200)),
                ('leak_visibility_body', models.CharField(max_length=200)),
                ('severe_corrosion_flanges', models.CharField(max_length=200)),
                ('visibility_crack_nuts_bolt', models.CharField(max_length=200)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
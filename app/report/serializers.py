"""
Serializers for report APIs
"""
from rest_framework import serializers

from core.models import (
    Report,
    Job,
)


class JobSerializer(serializers.ModelSerializer):
    """Serializer for jobids."""

    class Meta:
        model = Job
        fields = ['id', 'name']
        read_only_fields = ['id']


class ReportSerializer(serializers.ModelSerializer):
    """Serializer for reports."""
    jobs = JobSerializer(many=True, required=False)

    class Meta:
        model = Report
        fields = ['id',
                  'job_id',
                  'clients',
                  'client_logo',
                  'location',
                  'year',
                  'month',
                  'initial',
                  'po_num',
                  'hub',
                  'platform_location',
                  'survey_date',
                  'inspection_by',
                  'valve_tag_no',
                  'valve_description',
                  'valve_type',
                  'functions',
                  'valve_size',
                  'valve_make',
                  'actuator_make',
                  'valve_photo',
                  'p_and_id_no',
                  'mal_sof',
                  'mal_sof_others',
                  'mal',
                  'mal_warn',
                  'fluid_type',
                  'presure_upstream',
                  'pressure_downstream',
                  'flow_direction',
                  'u3',
                  'u2',
                  'u1',
                  'va',
                  'vb',
                  'vc',
                  'vd',
                  'd1',
                  'd2',
                  'd3',
                  'result',
                  'estimated_leak_rate',
                  'color_code',
                  'reason_not_tested',
                  'discussion_result',
                  'recommended_action',
                  'maintenance_his',
                  'avail_nameplate_tagno',
                  'presence_downstream',
                  'leak_visibility_body',
                  'severe_corrosion_flanges',
                  'visibility_crack_nuts_bolt',
                  'jobs'
                  ]
        read_only_fields = ['id']

    def _get_or_create_jobs(self, jobs, report):
        """Handle getting or creating jobs as needed"""
        auth_user = self.context['request'].user
        for job in jobs:
            job_obj, created = Job.objects.get_or_create(
                user=auth_user,
                **job,
            )
            report.jobs.add(job_obj)

    def create(self, validated_data):
        """Create a report."""
        jobs = validated_data.pop('jobs', [])
        report = Report.objects.create(**validated_data)
        self._get_or_create_jobs(jobs, report)

        return report

    def update(self, instance, validated_data):
        """Update a report"""
        jobs = validated_data.pop('jobs', None)
        if jobs is not None:
            instance.jobs.clear()
            self._get_or_create_jobs(jobs, instance)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class ReportDetailSerializer(ReportSerializer):
    """Serializer for report detail view."""

    class Meta(ReportSerializer.Meta):
        fields = ReportSerializer.Meta.fields + ['id']

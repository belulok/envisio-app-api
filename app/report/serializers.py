"""
Serializers for report APIs
"""
from rest_framework import serializers

from core.models import Report


class ReportSerializer(serializers.ModelSerializer):
    """Serializer for reports."""

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
                  ]
        read_only_fields = ['id']


class ReportDetailSerializer(ReportSerializer):
    """Serializer for report detail view."""

    class Meta(ReportSerializer.Meta):
        fields = ReportSerializer.Meta.fields + ['description']

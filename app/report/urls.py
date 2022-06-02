"""
URL mappings for the report app.
"""
from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from report import views


router = DefaultRouter()
router.register('reports', views.ReportViewSet)
router.register('jobs', views.JobViewSet)

app_name = 'report'

urlpatterns = [
    path('', include(router.urls)),
]

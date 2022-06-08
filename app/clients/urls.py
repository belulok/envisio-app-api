"""
URL mappings for the client app
"""
from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from clients import views

router = DefaultRouter()
router.register('clients', views.ClientsViewSet)

app_name = 'clients'

urlpatterns = [
    path('', include(router.urls)),
]

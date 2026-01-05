from django.urls import path
from . import views

urlpatterns = [
    path('sensor', views.ingest, name='sensor'),  # must match /api/sensor
    path('data/', views.list_data, name='list_data'),
]
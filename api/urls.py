from django.urls import path
from django.http import HttpResponse
from . import views

urlpatterns = [
    path("ping", lambda r: HttpResponse("pong")),
    path('sensor', views.ingest, name='sensor'),  # must match /api/sensor
    path('data/', views.list_data, name='list_data'),
    path('login', views.login),
]
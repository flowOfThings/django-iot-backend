from django.urls import path
from . import views

urlpatterns = [
    path('ingest/', views.ingest, name='ingest'),
    path('data/', views.list_data, name='list_data'),
]
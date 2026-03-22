# scanner/urls.py
from django.urls import path
from .views import scan_file

urlpatterns = [
    path('upload/', scan_file),
]

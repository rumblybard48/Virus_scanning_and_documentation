from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse  # Add this line

# Optional homepage view
def home(request):
    return JsonResponse({"message": "Welcome to the DMS API"})

urlpatterns = [
    path('', home),  # This catches visits to http://127.0.0.1:8000/
    path('admin/', admin.site.urls),
    path('api/', include('scanner.urls'))
]


from django.contrib import admin
from django.urls import path, include  # Přidání include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('partners.urls')),  # Připojení URL aplikace partners
]

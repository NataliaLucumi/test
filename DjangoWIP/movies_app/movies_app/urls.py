# furniture_app/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('staticpages/', include('staticpages.urls')),
    path('dynamicpages/', include('dynamicpages.urls')),
    path('api/', include('api.urls')),
]

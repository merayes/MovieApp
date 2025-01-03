# project_name/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),  # Kullanıcı ile ilgili işlemler
    path('movies/', include('movieapp.urls')),   # movieapp URLs'i dahil edin
]

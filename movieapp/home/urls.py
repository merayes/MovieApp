from django.urls import path
from . import views  # home uygulamasındaki view'ları dahil ediyoruz

urlpatterns = [
    path('', views.home, name='home'),  # Ana sayfa route'u
    path('sayfa-hakkinda/', views.sayfa_hakkinda, name='sayfa_hakkinda'),
]
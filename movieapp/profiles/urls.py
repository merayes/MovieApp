from django.urls import path
from .views import profile  # profile_view yerine profile
from . import views


urlpatterns = [
    path('edit_profile/', views.profile, name='edit_profile'),
    path('', views.profile_view, name='profile'),  # Kendi profilini görüntüleme
    path('<str:username>/', views.user_profile, name='user_profile'),
    
]

from django.urls import path
from .views import movie_list

from . import views

urlpatterns = [
    path('', movie_list, name='movie_list'),  # movies ana URL'sine bir view atandı
    path('search/', views.movie_search, name='movie_search'),
    path('popular/', views.popular_movies, name='popular_movies'),
    path('movie/<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('reply-comment/<int:comment_id>/', views.reply_comment, name='reply_comment'),
    path('comments/<int:comment_id>/toggle-like/', views.toggle_like, name='toggle_like'),
    path('yorumlar/', views.user_comments, name='user_comments'),
    path('genres/', views.movies_by_genre, name='movies_by_genre'),
    path('watchlist/', views.user_watchlist, name='user_watchlist'),
    path('watchlist/add/<int:movie_id>/', views.add_to_watchlist, name='add_to_watchlist'),
    path('watchlist/remove/<int:movie_id>/', views.remove_from_watchlist, name='remove_from_watchlist'),
]

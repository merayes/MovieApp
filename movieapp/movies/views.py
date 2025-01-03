from django.shortcuts import render, redirect, get_object_or_404
import requests
from .models import Movie
from .tmdb import search_movies, get_popular_movies, get_movie_details
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Comment, Watchlist
from .forms import CommentForm
from django.http import JsonResponse
from .tmdb import get_genres, get_movie_videos



API_KEY = '6323f247e48b24d19e93956ab9e29ff6'  # Kendi API anahtarınızı buraya koyun
BASE_URL = 'https://api.themoviedb.org/3/'

def movie_list(request):
    movies = Movie.objects.all()
    return render(request, 'movies/movie_list.html', {'movies': movies})

def get_movie_search_results(query):
    url = f"{BASE_URL}search/movie"
    params = {
        'api_key': API_KEY,
        'language': 'en-US',
        'query': query,
        'page': 1,
    }
    response = requests.get(url, params=params)
    data = response.json()  # Bu JSON yapısı 'results' anahtarını içermelidir
    return data

def movie_search(request):
    query = request.GET.get('query', '')
    if query:
        movies = get_movie_search_results(query)  # movie search results al
        if 'results' in movies:  # 'results' anahtarını kontrol et
            return render(request, 'movies/movie_search.html', {'movies': movies})
        else:
            return render(request, 'movies/movie_search.html', {'movies': None})
    return render(request, 'movies/movie_search.html', {'movies': None})

# Popüler filmleri alacak fonksiyon
def get_popular_movies():
    url = f"{BASE_URL}movie/popular"
    params = {
        'api_key': API_KEY,
        'language': 'en-US',
        'page': 1,
    }
    response = requests.get(url, params=params)
    data =response.json()
    return data

def popular_movies(request):
    movies = get_popular_movies()
    if 'results' in movies:
        return render(request, 'movies/popular_movies.html', {'movies': movies})
    else:
        return render(request, 'movies/popular_movies.html', {'movies': None})


@login_required
def movie_detail(request, movie_id):
    # TMDb API'den film detaylarını al
    movie = get_movie_details(movie_id)  # Daha önce yazdığınız API fonksiyonunu kullanın

    # Fragmanları al
    videos = get_movie_videos(movie_id)
    trailer = None

    # YouTube fragmanını filtrele
    for video in videos:
        if video['site'] == 'YouTube' and video['type'] == 'Trailer':
            trailer = f"https://www.youtube.com/embed/{video['key']}"
            break



    # Yorumlar ve form
    comments = Comment.objects.filter(movie_id=movie_id, parent=None).order_by('-created_at')
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.movie_id = movie_id
            comment.save()
            return redirect('movie_detail', movie_id=movie_id)
    else:
        form = CommentForm()

    return render(request, 'movies/movie_detail.html', {
        'movie': movie,
        'comments': comments,
        'form': form,
        'trailer': trailer,  # Fragman URL'sini template'e gönder
    })


@require_POST
def toggle_like(request, comment_id):
    """Handle the like/unlike action for comments."""
    if not request.user.is_authenticated:
        return JsonResponse({
            'success': False, 
            'message': 'User not authenticated'
        }, status=403)

    try:
        comment = get_object_or_404(Comment, id=comment_id)
        
        if request.user in comment.likes.all():
            comment.likes.remove(request.user)
            liked = False
        else:
            comment.likes.add(request.user)
            liked = True

        return JsonResponse({
            'success': True,
            'liked': liked,
            'like_count': comment.likes.count()
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=400)
    
def like_comment(request, comment_id):
    if request.user.is_authenticated:
        comment = get_object_or_404(Comment, id=comment_id)
        if request.user in comment.likes.all():
            comment.likes.remove(request.user)  # Beğeniyi kaldır
            liked = False
        else:
            comment.likes.add(request.user)  # Beğeni ekle
            liked = True
        return JsonResponse({'liked': liked, 'like_count': comment.likes.count()})
    else:
        return JsonResponse({'error': 'You must be logged in to like comments.'}, status=403)

def reply_comment(request, comment_id):
    if request.method == "POST":
        parent_comment = Comment.objects.get(id=comment_id)
        reply_text = request.POST.get('reply_text')
        if reply_text:
            Comment.objects.create(
                user=request.user,
                movie_id=parent_comment.movie_id,
                text=reply_text,
                parent=parent_comment
            )
        return redirect('movie_detail', movie_id=parent_comment.movie_id)
    
@login_required
def user_comments(request):
    """Kullanıcının yaptığı yorumları listeleyen view."""
    comments = Comment.objects.filter(user=request.user).order_by('-created_at')

    # movie_id ile film başlıklarını eşleştiren bir sözlük oluştur
    movie_titles = {
        comment.movie_id: Movie.objects.filter(id=comment.movie_id).first().title
        if Movie.objects.filter(id=comment.movie_id).exists() else "Bilinmeyen Film"
        for comment in comments
    }

    return render(request, 'movies/user_comments.html', {'comments': comments, 'movie_titles': movie_titles})

def movies_by_genre(request):
    # Tüm türleri al
    genres = get_genres()
    genre_movies = {}

    # Her tür için popüler filmleri çek
    for genre in genres:
        genre_id = genre['id']
        url = f"{BASE_URL}discover/movie"
        params = {
            'api_key': API_KEY,
            'language': 'tr-TR',
            'with_genres': genre_id,
            'sort_by': 'popularity.desc',
            'page': 1,
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            genre_movies[genre['name']] = response.json().get('results', [])

    return render(request, 'movies/movies_by_genre.html', {'genre_movies': genre_movies})


@login_required
def add_to_watchlist(request, movie_id):
    movie_title = request.GET.get('movie_title', '')
    if not Watchlist.objects.filter(user=request.user, movie_id=movie_id).exists():
        Watchlist.objects.create(user=request.user, movie_id=movie_id, movie_title=movie_title)
        return JsonResponse({'success': True, 'message': 'Film izleme listesine eklendi!'})
    return JsonResponse({'success': False, 'message': 'Film zaten izleme listesinde.'})

@login_required
def remove_from_watchlist(request, movie_id):
    watchlist_item = Watchlist.objects.filter(user=request.user, movie_id=movie_id).first()
    if watchlist_item:
        watchlist_item.delete()
        return JsonResponse({'success': True, 'message': 'Film izleme listesinden kaldırıldı!'})
    return JsonResponse({'success': False, 'message': 'Film izleme listesinde bulunamadı.'})

@login_required
def user_watchlist(request):
    watchlist = Watchlist.objects.filter(user=request.user).order_by('-added_at')
    return render(request, 'movies/watchlist.html', {'watchlist': watchlist})
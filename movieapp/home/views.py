# home/views.py
import requests
from django.shortcuts import render
from movies.tmdb import search_movies
from movies.tmdb import search_movies  # Popüler ve arama için gereken fonksiyonlar
from movies.models import Comment
from django.contrib.auth.decorators import login_required

API_KEY = '6323f247e48b24d19e93956ab9e29ff6'  # TMDb API anahtarınızı buraya koyun
BASE_URL = 'https://api.themoviedb.org/3/'

# Tüm popüler filmleri alacak fonksiyon
def get_all_movies():
    url = f"{BASE_URL}movie/popular"
    params = {
        'api_key': API_KEY,
        'language': 'en-US',
        'page': 1,  # Sayfa numarasını burada belirtebilirsiniz
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data
# Ana sayfa view'ı
def home(request):
    query = request.GET.get('q')  # Arama sorgusunu al
    if query:
        movies = search_movies(query)  # Eğer sorgu varsa TMDb API'den arama yap
        searching = True  # Arama yapıldığını göstermek için bir flag
    else:
        movies = get_all_movies()  # Eğer sorgu yoksa popüler filmleri getir
        searching = False
    
    film_news = get_film_news()  # Film haberlerini getir


    return render(request, 'home/home.html', {
        'movies': movies,
        'query': query,
        'searching': searching,
        'film_news': film_news
    })

def sayfa_hakkinda(request):
    return render(request, 'home/sayfahakkinda.html')

def get_film_news():
    api_key = "cd148eca4ee24e0db6328824b5ab3c1c"
    url = f"https://newsapi.org/v2/everything?q=movies&language=tr&apiKey={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get("articles", [])
    return []
import requests
from django.conf import settings

# TMDb API anahtarınızı settings.py dosyasından alıyoruz
API_KEY = settings.TMDB_API_KEY
BASE_URL = 'https://api.themoviedb.org/3/'

def get_movie_details(movie_id):
    url = f"{BASE_URL}movie/{movie_id}"
    params = {
        'api_key': API_KEY,
        'language': 'tr-TR',
    }
    response = requests.get(url, params=params)
    return response.json()

def search_movies(query):
    url = f"https://api.themoviedb.org/3/search/movie"
    params = {
        'api_key': API_KEY,
        'query': query
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    return None

def get_popular_movies():
    url = f"{BASE_URL}movie/popular"
    params = {
        'api_key': API_KEY,
        'language': 'tr-TR',
        'page': 1,
    }
    response = requests.get(url, params=params)
    return response.json()

def get_genres():
    url = f"{BASE_URL}genre/movie/list"
    params = {
        'api_key': API_KEY,
        'language': 'tr-TR',
    }
    response = requests.get(url, params=params)
    return response.json().get('genres', [])

def get_movie_videos(movie_id):
    """
    TMDb API'den bir filmin videolarını (fragman dahil) çeker.
    """
    url = f"{BASE_URL}movie/{movie_id}/videos"
    params = {
        'api_key': API_KEY,
        'language': 'tr-TR'
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json().get('results', [])
    return []

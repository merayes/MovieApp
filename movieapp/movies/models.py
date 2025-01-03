from django.db import models
from django.contrib.auth.models import User


class Movie(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    release_date = models.DateField()
    rating = models.FloatField()

    def __str__(self):
        return self.title

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Yorumu yapan kullanıcı
    movie_id = models.IntegerField()  # Yorumun ait olduğu filmin TMDb ID'si
    text = models.TextField()  # Yorumun içeriği
    created_at = models.DateTimeField(auto_now_add=True)  # Yorumun oluşturulma tarihi
    likes = models.ManyToManyField(User, related_name='liked_comments', blank=True)  # Beğeniler
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')  # Yanıtlar
        

    def __str__(self):
        return f"{self.user.username} - {self.movie_id}"
    
    @property
    def like_count(self):
        return self.likes.count()
    

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie_id = models.IntegerField()  # TMDb film ID'si
    movie_title = models.CharField(max_length=255)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.movie_title}"
from django.contrib import admin
from .models import Movie

admin.site.register(Movie)

from .models import Comment  # Comment modelinizi içe aktarın

class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'text', 'created_at', 'like_count')
    search_fields = ('user__username', 'text')
    readonly_fields = ('like_count',)

    def like_count(self, obj):
        return obj.likes.count()
    like_count.short_description = 'Number of Likes'

# Modeli admin paneline kaydedin
admin.site.register(Comment, CommentAdmin)

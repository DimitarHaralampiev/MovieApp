from django.contrib import admin

from movie.models import Movie, Comment, Rating

admin.site.register(Movie)
admin.site.register(Comment)
admin.site.register(Rating)

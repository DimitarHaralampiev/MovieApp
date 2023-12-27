from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Avg
from django.utils import timezone

from movie.consts import GENRE
from movie.utils import user_directory_path


class Rating(models.Model):
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])

    def __str__(self):
        return f"{self.user.username} - {self.movie.title}"


class Comment(models.Model):
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text


class Movie(models.Model):
    title = models.CharField('TITLE', max_length=255, unique=True)
    description = models.TextField('DESCRIPTION', blank=True)
    release_date = models.DateField('RELEASE DATE', default=timezone.now())
    director = models.CharField('DIRECTOR', max_length=255)
    genre = models.CharField('GENRE', choices=GENRE, max_length=20, default=None)
    cover_image = models.ImageField('COVER IMAGE', upload_to=user_directory_path, blank=True)
    is_favorite = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.title

    def average_rating(self):
        return f"{self.ratings.aggregate(Avg('value'))['value__avg']}"

    class Meta:
        indexes = [
            models.Index(fields=['title', 'director', 'genre']),
        ]

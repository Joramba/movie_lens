from django.db import models
from django.conf import settings


class Genre(models.Model):
    name = models.CharField(max_length=300)

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=1000)
    year = models.IntegerField()
    director = models.CharField(max_length=300)
    imdbLink = models.URLField()
    image = models.CharField(max_length=100)
    description = models.TextField(default='Default description')
    genres = models.ManyToManyField(Genre)

    def __str__(self):
        return self.title


class Rating(models.Model):
    value = models.IntegerField()
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user_review = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

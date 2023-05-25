from django.db import models
from django.conf import settings


class Genre(models.Model):
    name = models.CharField(max_length=300)

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=1000)
    imdbid = models.CharField(max_length=100, default='N/A')
    year = models.IntegerField(default=0)
    img_url = models.URLField(max_length=600, default='N/A')
    audience_rating = models.FloatField()
    critic_rating = models.FloatField()
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

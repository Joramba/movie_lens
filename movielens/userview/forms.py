from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth import login
from .models import Movie, Genre, Rating, Comment


class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class RatingForm(forms.ModelForm):
    movie = forms.ModelChoiceField(
        queryset=Movie.objects.all(), empty_label="Choose a movie")
    value = forms.IntegerField(min_value=1, max_value=5)

    class Meta:
        model = Rating
        fields = ('movie', 'rating')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(RatingForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        rating = super().save(commit=False)
        rating.user = self.user

        if commit:
            rating.save()
        return rating


class CommentForm(forms.ModelForm):
    comment = forms.CharField(widget=forms.Textarea(),
                                  label='Your Review')

    class Meta:
        model = Comment
        fields = ('comment',)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.movie = kwargs.pop('movie', None)
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['comment'].label = 'Your Review'  

    def save(self, commit=True):
        comment = super().save(commit=False)
        comment.user = self.user
        comment.movie = self.movie

        if commit:
            comment.save()
        return comment


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ('title', 'year', 'director', 'imdbLink', 'image', 'description', 'genres')


class MovieSearchForm(forms.Form):
    genre_choices = [(genre.name, genre.name) for genre in Genre.objects.all()]
    genre = forms.ChoiceField(choices=genre_choices, required=False, initial='')
    title = forms.CharField(required=False)
    rating = forms.FloatField(required=False)
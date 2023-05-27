from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.template import loader
from .models import Movie, Genre, Rating, Comment
from django.views import generic
from django.shortcuts import get_object_or_404
from .forms import NewUserForm, RatingForm, CommentForm, MovieForm

from django.contrib import messages

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import login


def index(request: HttpRequest):
    user = request.user
    print(user)

    if (request.user.is_anonymous):
        ratings = None
    else:
        ratings = Rating.objects.filter(user=user)

    movies = Movie.objects.order_by('-title')
    template = loader.get_template('userview/index.html')

    object_list = Movie.objects.all()
    page_num = request.GET.get('page', 1)

    paginator = Paginator(object_list, 10)  # 1 employees per page

    try:
        page_obj = paginator.page(page_num)
    except PageNotAnInteger:
        # if page is not an integer, deliver the first page
        page_obj = paginator.page(1)
    except EmptyPage:
        # if the page is out of range, deliver the last page
        page_obj = paginator.page(paginator.num_pages)

    context = {
        'movies': movies,
        'ratings': ratings,
        'page_obj': page_obj
    }

    return HttpResponse(template.render(context, request))


def edit_movie(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)

    if request.method == 'POST':
        form = MovieForm(request.POST, instance=movie)
        if form.is_valid():
            form.save()
            return redirect('movie', movie_id=movie.id)
    else:
        form = MovieForm(instance=movie)

    return render(request, 'userview/edit_movie.html', {'form': form})


def view_genre(request: HttpRequest, genre_id):
    genres = Genre.objects.order_by('-name')
    template = loader.get_template('userview/genre.html')

    genre = get_object_or_404(Genre, id=genre_id)
    context = {
        'genre': genre
    }

    return HttpResponse(template.render(context, request))


def view_movie(request: HttpRequest, movie_id):
    template = loader.get_template('userview/movie.html')

    movie = get_object_or_404(Movie, id=movie_id)
    ratings = Rating.objects.filter(movie=movie)
    comments = Comment.objects.filter(movie=movie)

    context = {
        'movie': movie,
        'ratings': ratings,
        'comments': comments
    }
    return HttpResponse(template.render(context, request))


def add_movie(request):
    if request.method == 'POST':
        form = MovieForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')  # Redirect to the movie list page after successful addition
    else:
        form = MovieForm()

    return render(request, 'userview/add_movie.html', {'form': form})


def add_rating(request: HttpRequest):
    if request.method == 'POST':
        form = RatingForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = RatingForm(user=request.user)
    return render(request, 'userview/rating.html', {'form': form})


def create_comment(request: HttpRequest, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)

    if request.method == 'POST':
        form = CommentForm(request.POST, user=request.user, movie=movie)
        if form.is_valid():
            form.save()
            return redirect('movie', movie_id=movie.id)
    else:
        form = CommentForm(user=request.user, movie=movie)

    return render(request, 'userview/comment.html', {'form': form, 'movie': movie})


class IndexView(generic.ListView):
    template_name = 'userview/index.html'
    context_object_name = 'movies'

    def get_queryset(self):
        return Movie.objects.order_by('-title')


class MovieView(generic.DetailView):
    model = Movie
    template_name = 'userview/movie.html'


class GenreView(generic.DetailView):
    model = Genre
    template_name = 'userview/genre.html'


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("login")
        messages.error(
            request, "Unsuccessful registration. Invalid information.")
    else:
        form = NewUserForm()
        return render(request=request, template_name="userview/register.html", context={"register_form": form})

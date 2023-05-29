from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.template import loader
from .models import Movie, Genre, Rating, Comment
from django.views import generic
from django.shortcuts import get_object_or_404
from .forms import NewUserForm, RatingForm, CommentForm, MovieForm, MovieSearchForm

from django.contrib import messages

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import login
from django.db.models import Max


def get_highest_rated_movies(user):
    highest_ratings = Rating.objects.filter(user=user).aggregate(Max('rating'))
    highest_rating = highest_ratings['rating__max']
    highest_rated_movies = Movie.objects.filter(rating__rating=highest_rating, rating__user=user)
    return highest_rated_movies


def index(request: HttpRequest):
    user = request.user
    print(user)


    if (request.user.is_anonymous):
        ratings = None
        highest_rated_movies = None
    else:
        ratings = Rating.objects.filter(user=user)
        highest_rated_movies = get_highest_rated_movies(user=user)

    movies = Movie.objects.order_by('-title')
    template = loader.get_template('userview/index.html')

    object_list = Movie.objects.all()
    page_num = request.GET.get('page', 1)

    paginator = Paginator(object_list, 12)  # 12 employees per page

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
        'page_obj': page_obj,
        'highest_rated_movies': highest_rated_movies
    }

    return HttpResponse(template.render(context, request))

def movie_search(request):
    form = MovieSearchForm()

    if request.method == 'POST':
        form = MovieSearchForm(request.POST)
        if form.is_valid():
            if form.is_valid():
                genre = form.cleaned_data.get('genre')
                title = form.cleaned_data.get('title')
                rating = form.cleaned_data.get('rating')

                movies = Movie.objects.all()

                if genre:
                    movies = movies.filter(genres__name__icontains=genre)
                if title:
                    movies = movies.filter(title__icontains=title)
                if rating is not None:
                    movies = movies.filter(audience_rating__gte=rating)


            return render(request, 'userview/movie_search_results.html', {'form': form, 'movies': movies})

    return render(request, 'userview/movie_search.html', {'form': form})



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

    similar_movies = movie.get_similar_movies()[:5]

    context = {
        'movie': movie,
        'ratings': ratings,
        'comments': comments,
        'similar_movies':similar_movies
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
        print(1)
        form = CommentForm(request.POST, user=request.user, movie=movie)
        if form.is_valid():
            print(2)
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

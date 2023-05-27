"""
URL configuration for movielens project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import include, path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.index, name="index"),
    path("genre/<int:genre_id>", views.view_genre, name="genre"),
    path("movie/<int:movie_id>", views.view_movie, name="movie"),
    path("rating/", views.add_rating, name="rating"),
    path('movie/edit/<int:movie_id>', views.edit_movie, name='edit_movie'),
    path('movie/add/', views.add_movie, name='add_movie'),
    path("comment/create/<int:movie_id>", views.create_comment, name="comment"),
    path("register/", views.register_request, name="register"),
    path('login/', auth_views.LoginView.as_view(template_name='userview/login.html'), name="login"),
    path('logout/', auth_views.LogoutView.as_view(template_name='userview/logout.html'), name="logout")

    # path("login", views.login_request, name="login")
    # path("", views.IndexView.as_view(), name="index"),
    # path("genre/<int:pk>", views.GenreView.as_view(), name="index"),
    # path("movie/<int:pk>", views.MovieView.as_view(), name="index"),
]

#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import json
from django.contrib.auth.hashers import make_password


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'movielens.settings')
import django
django.setup()

from django.contrib.auth.models import User


def import_users():
    directory_path = '../data/picked_users/' 

    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)

        with open(file_path, 'r') as file:
            user_data = json.load(file)

        user_id = user_data['user_id']
        password = make_password(user_data['password'])
        first_name = user_data['first_name']
        last_name = user_data['last_name']
        username = user_data['username']

        # Create or update the user object
        user, created = User.objects.update_or_create(
            id=user_id,
            defaults={
                'password': password,
                'first_name': first_name,
                'last_name': last_name,
                'username': username
            }
        )

        print(f'User {username} imported.')

    print('Data import completed.')


def import_movies():
    directory_path = '../data/picked_movies/'  # Replace with the actual directory path

    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)

        with open(file_path, 'r', encoding='latin-1') as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError as e:
                print(f"Error loading JSON from file {file_path}: {e}")
                continue

        title = data['title']
        director = data['director']
        year = data['year']
        imdbLink = data['imdbLink']
        image = data['image']
        description = data['description']
        genres = data['genre'].split(', ')

        movie = Movie(
                title=title,
                director=director,
                year=year,
                imdbLink=imdbLink,
                image=image,
                description=description
            )

        movie.save()

        for genre_name in genres:
            genre_objects = Genre.objects.filter(name=genre_name)
            if genre_objects.exists():
                genre = genre_objects.first()
            else:
                genre = Genre.objects.create(name=genre_name)
            movie.genres.add(genre)

        print(f'Movie {title} imported.')


    print('Data import completed.')

def import_ratings():
    directory_path = '../data/picked_ratings/'  # Replace with the actual directory path

    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)

        with open(file_path, 'r') as file:
            ratings_data = json.load(file)

        user_id = int(ratings_data['user_id'])
        movie_id = int(ratings_data['movie_id'])
        rating = float(ratings_data['rating'])

        try:
            user = User.objects.get(id=user_id)
            movie = Movie.objects.get(id=movie_id)

            rating_obj, created = Rating.objects.get_or_create(
                user=user,
                movie=movie,
                defaults={'rating': rating}
            )

            if not created:
                rating_obj.rating = rating
                rating_obj.save()

            print(f'Successfully imported rating: {rating}')

        except User.DoesNotExist:
            sprint(f'Not added imported user: {rating}')

        except Movie.DoesNotExist:
           print(f'No added rating: {rating}')

    print(f'Successfully imported data')


def import_comments():
    file_path = '../data/picked_comments.json'  # Replace with the actual file path

    with open(file_path, 'r') as file:
        comments_data = json.load(file)

    for comment_data in comments_data:
        user_id = int(comment_data['user'])
        movie_id = int(comment_data['movie'])
        comment_text = comment_data['comment']
        timestamp = datetime.fromtimestamp(int(comment_data['timestamp']))

        try:
            user = User.objects.get(id=user_id)
        except ObjectDoesNotExist:
            print(f"User with id {user_id} does not exist. Skipping comment.")
            continue
        
        try:
            movie = Movie.objects.get(id=movie_id)
        except ObjectDoesNotExist:
            print(f"Movie with id {movie_id} does not exist. Skipping comment.")
            continue

        comment = Comment(user=user, movie=movie, comment=comment_text, timestamp=timestamp)
        comment.save()

        print(f'Successfully imported comment: {comment}')


    print('Data import completed.')

    
def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'movielens.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()



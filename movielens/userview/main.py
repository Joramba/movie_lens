import os
import json
import django

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'movielens.settings')
django.setup()


from django.contrib.auth.models import User
from userview.models import Movie, Comment
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist

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


if __name__ == '__main__':
    import_comments()

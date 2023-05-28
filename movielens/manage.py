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



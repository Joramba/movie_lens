# Generated by Django 4.2 on 2023-05-28 20:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userview', '0005_rename_movie_rating_movie_id_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rating',
            old_name='movie_id',
            new_name='movie',
        ),
        migrations.RenameField(
            model_name='rating',
            old_name='user_id',
            new_name='user',
        ),
    ]
# Generated by Django 4.2 on 2023-05-25 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userview', '0002_movie_audience_rating_movie_critic_rating_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='audience_rating',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='movie',
            name='critic_rating',
            field=models.FloatField(),
        ),
    ]

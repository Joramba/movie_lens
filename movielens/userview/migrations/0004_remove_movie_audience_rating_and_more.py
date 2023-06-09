# Generated by Django 4.2 on 2023-05-28 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userview', '0003_alter_movie_audience_rating_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='audience_rating',
        ),
        migrations.RemoveField(
            model_name='movie',
            name='critic_rating',
        ),
        migrations.RemoveField(
            model_name='movie',
            name='imdbid',
        ),
        migrations.RemoveField(
            model_name='movie',
            name='img_url',
        ),
        migrations.AddField(
            model_name='movie',
            name='description',
            field=models.TextField(default='Default description'),
        ),
        migrations.AddField(
            model_name='movie',
            name='director',
            field=models.CharField(default='NULL', max_length=300),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='movie',
            name='image',
            field=models.CharField(default='N/A', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='movie',
            name='imdbLink',
            field=models.URLField(default='N/A'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='movie',
            name='year',
            field=models.IntegerField(),
        ),
    ]

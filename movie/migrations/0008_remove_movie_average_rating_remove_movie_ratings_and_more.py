# Generated by Django 5.0 on 2023-12-21 18:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0007_movie_average_rating_movie_total_ratings'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='average_rating',
        ),
        migrations.RemoveField(
            model_name='movie',
            name='ratings',
        ),
        migrations.RemoveField(
            model_name='movie',
            name='total_ratings',
        ),
        migrations.RemoveField(
            model_name='rating',
            name='value',
        ),
    ]

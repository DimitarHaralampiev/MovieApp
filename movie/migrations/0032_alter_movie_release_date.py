# Generated by Django 5.0 on 2023-12-27 16:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0031_alter_movie_release_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='release_date',
            field=models.DateField(default=datetime.datetime(2023, 12, 27, 16, 38, 25, 767167, tzinfo=datetime.timezone.utc), verbose_name='RELEASE DATE'),
        ),
    ]

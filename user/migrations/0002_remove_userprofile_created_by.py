# Generated by Django 5.0 on 2023-12-20 17:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='created_by',
        ),
    ]

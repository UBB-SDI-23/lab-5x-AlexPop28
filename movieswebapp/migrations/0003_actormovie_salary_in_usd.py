# Generated by Django 4.1.7 on 2023-03-20 06:47

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("movieswebapp", "0002_actor_director_actormovie_movie_actors_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="actormovie",
            name="salary_in_usd",
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]

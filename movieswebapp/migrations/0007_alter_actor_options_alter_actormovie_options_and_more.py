# Generated by Django 4.2 on 2023-04-18 12:54

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("movieswebapp", "0006_actormovie_character_name"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="actor",
            options={"ordering": "name"},
        ),
        migrations.AlterModelOptions(
            name="actormovie",
            options={"ordering": "id"},
        ),
        migrations.AlterModelOptions(
            name="director",
            options={"ordering": "name"},
        ),
        migrations.AlterModelOptions(
            name="movie",
            options={"ordering": "name"},
        ),
    ]
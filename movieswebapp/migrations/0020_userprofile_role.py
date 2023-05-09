# Generated by Django 4.2 on 2023-05-09 07:09

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("movieswebapp", "0019_userprofile_marital_status"),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="role",
            field=models.CharField(
                choices=[
                    ("Regular", "regular"),
                    ("Moderator", "moderator"),
                    ("Admin", "admin"),
                ],
                default="regular",
                max_length=10,
            ),
        ),
    ]
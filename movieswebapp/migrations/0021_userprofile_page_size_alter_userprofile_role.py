# Generated by Django 4.2 on 2023-05-10 11:14

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("movieswebapp", "0020_userprofile_role"),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="page_size",
            field=models.IntegerField(
                choices=[(10, 10), (25, 25), (100, 100)], default=10
            ),
        ),
        migrations.AlterField(
            model_name="userprofile",
            name="role",
            field=models.CharField(
                choices=[
                    ("regular", "Regular"),
                    ("moderator", "Moderator"),
                    ("admin", "Admin"),
                ],
                default="regular",
                max_length=10,
            ),
        ),
    ]

# Generated by Django 4.2 on 2023-05-03 09:06

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("movieswebapp", "0018_rename_username_userprofile_user"),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="marital_status",
            field=models.CharField(
                choices=[
                    ("Single", "single"),
                    ("Married", "married"),
                    ("Divorced", "divorced"),
                    ("Widowed", "widowed"),
                ],
                default="single",
                max_length=20,
            ),
            preserve_default=False,
        ),
    ]
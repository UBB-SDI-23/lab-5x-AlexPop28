# Generated by Django 4.2 on 2023-05-01 14:33

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("movieswebapp", "0015_update_userprofile_foreign_key_values"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userprofile",
            name="username",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="profile",
                to=settings.AUTH_USER_MODEL,
                to_field="username",
            ),
        ),
    ]

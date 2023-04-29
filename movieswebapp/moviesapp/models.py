from typing import cast

from django.contrib.auth.models import User
from django.db import models


class Person(models.Model):
    name = models.CharField(max_length=100)
    alternative_name = models.CharField(max_length=100, blank=True)
    date_of_birth = models.DateField()
    birthplace = models.CharField(max_length=100)
    height_in_cm = models.IntegerField()

    def __str__(self) -> str:
        return self.name

    class Meta:
        abstract = True
        ordering = ["name", "id"]
        indexes = [models.Index(fields=["name", "id"])]


class Actor(Person):
    class Meta(Person.Meta):
        indexes = [models.Index(fields=["date_of_birth"])]


class Director(Person):
    pass


class Movie(models.Model):
    name = models.CharField(max_length=100)
    rating = models.FloatField()
    release_date = models.DateField()
    length_in_minutes = models.IntegerField()
    director = models.ForeignKey(Director, on_delete=models.CASCADE)
    actors = models.ManyToManyField(Actor, through="ActorMovie")

    class Meta:
        ordering = ["name", "id"]
        indexes = [models.Index(fields=["name", "id"])]

    def __str__(self) -> str:
        return self.name


class ActorMovie(models.Model):
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    screen_time_in_minutes = models.IntegerField()
    salary_in_usd = models.IntegerField()
    character_name = models.CharField(max_length=100)

    class Meta:
        unique_together = (("actor", "movie"),)
        ordering = ["id"]
        indexes = [models.Index(fields=["id"])]


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    bio = models.TextField(max_length=500)
    location = models.CharField(max_length=100)
    birthday = models.DateField(null=True, blank=True)
    gender = models.CharField(
        max_length=10,
        choices=(("male", "Male"), ("female", "Female"), ("other", "Other")),
    )
    validation_code = models.CharField(max_length=36)
    validation_expiry_date = models.DateTimeField()
    active = models.BooleanField()

    def __str__(self) -> str:
        return cast(str, self.user.username)

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


class Actor(Person):
    pass


class Director(Person):
    pass


class Movie(models.Model):
    name = models.CharField(max_length=100)
    rating = models.FloatField()
    release_date = models.DateField()
    length_in_minutes = models.IntegerField()
    director = models.ForeignKey(Director, on_delete=models.CASCADE)
    actors = models.ManyToManyField(Actor, through="ActorMovie")

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

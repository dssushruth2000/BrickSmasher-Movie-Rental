from django.db import models

class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"

class Movie(models.Model):
    title = models.CharField(max_length=100, unique=True)
    in_stock = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.title

class Checkout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.email} checked out {self.movie.title}"

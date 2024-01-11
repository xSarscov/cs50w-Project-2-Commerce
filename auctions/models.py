from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    category_name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    image = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.category_name

class Listing(models.Model):
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    image = models.TextField()
    category = models.ForeignKey(Category, related_name='category', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, related_name='owner', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.title} by {self.user.username}'
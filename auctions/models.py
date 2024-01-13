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
    is_active = models.BooleanField(default=True)
    user = models.ForeignKey(User, related_name='owner', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.title} by {self.user.username}'
    
class Bid(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    listing = models.ForeignKey(Listing, related_name='listing', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='bidder', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_winner = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'{self.amount} on {self.listing.title} by {self.user.username}'
    
class Watchlist(models.Model):
    listing = models.ManyToManyField(Listing)
    user = models.ForeignKey(User, related_name='proprietary', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.user.username}'s watchlist"
    
class Comments(models.Model):
    content = models.TextField()
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.listing.title}'s comments"
    
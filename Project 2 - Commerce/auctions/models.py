from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    watchlist = models.ManyToManyField("Listing", blank=True, related_name="watchlist")


class Listing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    title = models.CharField(max_length=64)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.CharField(max_length=64, blank=True)
    image_url = models.URLField(blank=True, default="https://media.istockphoto.com/id/1147544807/vector/thumbnail-image-vector-graphic.jpg?s=612x612&w=0&k=20&c=rnCKVbdxqkjlcs3xH87-9gocETqpspHFXu5dIGB4wuM=")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    description = models.CharField(max_length=256)
    timestamp = models.DateTimeField(auto_now_add=True)

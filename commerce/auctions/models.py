from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    id = models.BigAutoField(primary_key=True, null=False)

    def __str__(self):
        return f"{self.username}"

class Auction_listing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    is_active = models.BooleanField()
    listing_desc = models.CharField(max_length=1000)
    initial_bid = models.FloatField()
    current_bid = models.FloatField()
    # img asscociated with a listing
    creation_date = models.DateTimeField()
    listing_img = models.CharField(max_length=10000, blank=True)
    listing_title = models.CharField(max_length=150)
    listing_category = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return f"{self.listing_title, self.is_active, self.user}"

class Watchlist(models.Model):
    user_id = models.IntegerField()
    listing = models.ForeignKey(Auction_listing, on_delete=models.CASCADE, related_name="watchlist")

class Bid(models.Model):
    value = models.FloatField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="made_bids")
    listing = models.ForeignKey(Auction_listing, on_delete=models.CASCADE, related_name="bids")

    def __str__(self):
        return f"{self.user.username}, {self.listing.listing_title}, {self.value}"

class Comment(models.Model):
    content = models.CharField(max_length=400)
    creation_date = models.DateTimeField()
    listing = models.ForeignKey(Auction_listing, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")

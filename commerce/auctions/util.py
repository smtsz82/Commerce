import django.http
from django.db import models
from .models import Auction_listing, Watchlist

def is_valid(id):
    "Returns true if listing with id exists false otherwise"
    try:
        listing = Auction_listing.objects.get(id=id)
    except:
        return False
    return True

def watchlisted(user_id ,listing):
    # Returns watchlist id if user with "user_id" added listing "listing" to his watchlist
    try:
        added = Watchlist.objects.get(user_id=user_id, listing=listing)
        return added.id
    except:
        return None

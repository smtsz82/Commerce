import django.http
from django.db import models
from .models import Auction_listing, Watchlist, Bid


def is_valid(id):
    """Returns true if listing with id exists false otherwise"""
    try:
        listing = Auction_listing.objects.get(id=id)
    except:
        return False
    return True


def watchlisted(user_id, listing):
    # Returns watchlist id if user with "user_id" added listing "listing" to his watchlist
    try:
        added = Watchlist.objects.get(user_id=user_id, listing=listing)
        return added.id
    except:
        return None


def assign_error_message(listing):
    if not listing.is_active:
        return "This listing is closed and you can no longer comment or place bids on it"
    return None


def find_highest_username(listing):
    bids = Bid.objects.filter(listing=listing)
    # If there are no bids user has closed his auction without eny bids being placed
    if len(bids) == 0:
        return listing.user
    max_bid = bids[0]
    for bid in bids:
        if bid.value > max_bid.value:
            max_bid = bid
    return max_bid.user

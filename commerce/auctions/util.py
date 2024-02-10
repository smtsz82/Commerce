import django.http

from .models import Auction_listing

def is_valid(id):
    "Returns true if listing with id exists false otherwise"
    try:
        listing = Auction_listing.objects.get(id=id)
    except:
        return False
    return True

import datetime
from .util import *
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django import forms
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import Auction_listing, Bid, Watchlist, User, Comment


class New_listing(forms.Form):
    listing_title = forms.CharField(widget=forms.TextInput(
        attrs={"required": True, "class": "form-control", "placeholder": "listing title", "name": "listing_title"}))
    listing_description = forms.CharField(widget=forms.TextInput(
        attrs={"required": True, "class": "form-control", "placeholder": "listing description",
               "name": "listing_description"}))
    starting_bid = forms.IntegerField(widget=forms.NumberInput(
        attrs={"required": True, "class": "form-control", "placeholder": "starting price", "name": "initial_bid",
               "min": 0, "step": 0.01}))


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Auction_listing.objects.all()
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def new_listing(request):
    if request.method == "GET":
        return render(request, "auctions/create_listing.html", {
            "form": New_listing()
        })
    elif request.user.is_authenticated and request.method == "POST":
        form = New_listing(request.POST)
        if form.is_valid():
            listing_title = form.cleaned_data["listing_title"]
            listing_description = form.cleaned_data["listing_description"]
            initial_bid = form.cleaned_data["starting_bid"]
            listing_category = request.POST["category"]
            listing_img = request.POST["image_url"]
            user_id = request.user.id
            auction_listing = Auction_listing(user=User.objects.get(id=user_id), is_active=True,
                                              initial_bid=initial_bid, current_bid=initial_bid, listing_img=listing_img,
                                              listing_title=listing_title, listing_desc=listing_description,
                                              listing_category=listing_category, creation_date=datetime.datetime.now())
            auction_listing.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/create_listing.html", {
                "form": form
            })
    return render(request, "auctions/create_listing.html", {
        "form": New_listing(),
        "message": "Listing creation failed, please"
    })


def listing_page(request, id):
    if is_valid(id):
        listing = Auction_listing.objects.get(id=id)
        # All comments for given listing
        comments = Comment.objects.filter(listing=listing)
        user_id = request.user.id
        login_message = "to perform this action"
        # Check if listing is watchlisted for the current user
        wlisted = watchlisted(user_id, listing)
        if wlisted:
            message = "Remove from watchlist"
        else:
            message = "Add to watchlist"
        if request.method == "GET":
            success_message = None
            if not listing.is_active:
                # Find user who placed the highest bid on the auction
                highest_biding_user = find_highest_username(listing)
                if highest_biding_user.id == request.user.id:
                    success_message = f"Congratulations {highest_biding_user.username} you have won this auction !"
            return render(request, "auctions/listing_page.html", {
                "listing": listing,
                "success_message": success_message,
                "error_message": assign_error_message(listing),
                "watchlist_state": message,
                "comments": comments
            })
        if request.method == "POST" and request.POST["action"] == "watchlist" and request.user.is_authenticated:
            # if user had listing in his watchlist we remove it from database
            if wlisted:
                Watchlist.objects.filter(id=wlisted).delete()
            else:
                watchlist = Watchlist(user_id=user_id, listing=listing)
                watchlist.save()
            return HttpResponseRedirect(reverse("listing_page", args=(id,)))
        if request.method == "POST" and request.POST["action"] == "close_listing" and request.user.is_authenticated:
            # Mark listing "is_active" field as False
            listing.is_active = False
            listing.save(update_fields=["is_active"])
            return HttpResponseRedirect(reverse("listing_page", args=(id,)))
        if request.method == "POST" and request.POST["action"] == "place_bid" and request.user.is_authenticated:
            bid_value = float(request.POST["bid_price"])
            if bid_value > listing.initial_bid and bid_value > listing.current_bid:
                listing.current_bid = bid_value
                listing.save(update_fields=["current_bid"])
                bid = Bid(user=request.user, listing=listing, value=bid_value)
                bid.save()
                return render(request, "auctions/listing_page.html", {
                    "listing": listing,
                    "success_message": "Bid placed successfully",
                    "error_message": assign_error_message(listing),
                    "watchlist_state": message,
                    "comments": comments
                })
            return render(request, "auctions/listing_page.html", {
                "listing": listing,
                "error_message": f"Your bid must be highest than current highest bid ({listing.current_bid}) !",
                "watchlist_state": message,
                "comments": comments
            })
        if request.method == "POST" and request.POST["action"] == "place_comment" and request.user.is_authenticated:
            comment_content = request.POST["comment_content"]
            # If user typed something to the comment field we create a comment
            if comment_content:
                comment = Comment(content=comment_content, creation_date=datetime.datetime.now(), listing=listing,
                                  user=User.objects.get(id=user_id))
                comment.save()
                return HttpResponseRedirect(reverse("listing_page", args=(id,)))
            # Else we render the page again with a warning
            return render(request, "auctions/listing_page.html", {
                "listing": listing,
                "warning_message": "Your comment needs to have content in it !",
                "error_message": assign_error_message(listing),
                "watchlist_state": message,
                "comments": comments
            })
        # if user is not logged in and tries to perform action that requires it we render the page with a error message
        else:
            return render(request, "auctions/listing_page.html", {
                "listing": listing,
                "error_message": assign_error_message(listing),
                "login_message": login_message,
                "watchlist_state": message,
                "comments": comments
            })
    return render(request, "auctions/404.html")


@login_required
def watchlist(request):
    wlisted_listings = Watchlist.objects.filter(user_id=request.user.id)
    listings = [listing.listing for listing in wlisted_listings]
    return render(request, "auctions/watchlist.html", {
        "listings": listings
    })

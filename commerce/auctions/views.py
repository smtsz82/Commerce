import datetime
from .util import *
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django import forms
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import Auction_listing
from .models import User


# class NewTaskForm(forms.Form):
#     task = forms.TextInput(attrs={"class":"form-control"})

class New_listing(forms.Form):
    listing_title = forms.CharField(widget=forms.TextInput(attrs={"required": True, "class": "form-control", "placeholder": "listing title", "name": "listing_title"}))
    listing_description = forms.CharField(widget=forms.TextInput(attrs={"required": True, "class": "form-control", "placeholder": "listing description", "name": "listing_description"}))
    starting_bid = forms.IntegerField(widget=forms.NumberInput(attrs={"required": True, "class": "form-control", "placeholder": "starting price", "name": "initial_bid", "min": 0.0}))



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
            auction_listing = Auction_listing(user=User.objects.get(id=user_id), is_active=True, initial_bid=initial_bid, current_bid=initial_bid, listing_img=listing_img, listing_title=listing_title, listing_desc=listing_description, listing_category=listing_category, creation_date=datetime.datetime.now())
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
    if request.method == "GET":
        if is_valid(id):
            listing = Auction_listing.objects.get(id=id)
            return render(request, "auctions/listing_page.html", {
                "listing": listing
            })
        return render(request, "auctions/404.html")

from django.contrib.auth import authenticate, login, logout
from django import forms
from django.db import IntegrityError, OperationalError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from .models import User, AuctionCategory, AuctionBid, AuctionListing, AuctionComment

# Evaluate if the user is logged in with the @login_required decorator
from django.contrib.auth.decorators import login_required

# Check if there is a column with listing in database
from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import DatabaseError


class AuctionListingForm(forms.Form):
    title = forms.CharField(max_length=100,
                            required=True,
                            widget=forms.TextInput(attrs={"autofocus":True,
                                                          "class":"form-control col-md-6",
                                                          }))
    category = forms.ModelChoiceField(queryset=AuctionCategory.objects.all(),
                                      required=False,
                                      widget=forms.Select(attrs={"class": "form-select col-md-2",
                                                                 "aria-label": "category dropdown list"}))
    new_category = forms.CharField(max_length=100,
                                   required=False,
                                   widget=forms.TextInput(attrs={"class": "form-control col-md-4", "placeholder": "New category (optional)"}))
    description = forms.CharField(max_length=500,
                                    widget=forms.Textarea(attrs={"class":"form-control col-md-6 mb-3",
                                                                 "rows":5}))
    # Max img size set in settings.py
    image = forms.ImageField()
    price = forms.DecimalField(widget=forms.TextInput(attrs={"class":"form-control col-md-6",
                                                             "placeholder": "0.00 $"}))


class AuctionBidForm(forms.Form):
    bid_amount = forms.DecimalField(required=True,
                                    widget=forms.TextInput(attrs={"class":"form",
                                                                  "placeholder": "0.00 $"}))


def error(request):
    return HttpResponseRedirect(request, "auctions/error.html",{
        "information": "Unknown error"
    })
    

def index(request):
    all_listings = AuctionListing.objects.all()
    if not all_listings.exists():
        all_listings = None
    return render(request, "auctions/index.html",{
        "listings": all_listings
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


def listing(request, listing_id):   
    try:
        curr_listing = get_object_or_404(AuctionListing, pk=listing_id)
        form = AuctionBidForm()
        return render(request, "auctions/listing.html", {
            "form": form,
            "listing": curr_listing
        })
    except AuctionListing.DoesNotExist:
        return render(request, "aucitons/error.html", {
            "information": "Listing not found"
        })
    

@login_required
def create_listing(request):
    '''Using form object and cleaned_data:
     - prevent from SQL injection
     - validate the input
     - handle errors
     - make core more modular
     For images it make size, type and name validation'''
    if request.method == 'POST':
        form = AuctionListingForm(request.POST, request.FILES or None)
        if form.is_valid():
            title           = form.cleaned_data["title"]
            category        = form.cleaned_data["category"]
            new_category    = form.cleaned_data["new_category"]
            if not category and not new_category:
                category, _ = AuctionCategory.objects.get_or_create(title="Others")
            elif new_category:
                category, _ = AuctionCategory.objects.get_or_create(title=new_category)
            description     = form.cleaned_data["description"]
            image           = form.cleaned_data["image"]
            price           = form.cleaned_data["price"]
            user            = request.user
            # Create a new listing
            new_listing = AuctionListing.objects.create(title=title,
                                                        description=description,
                                                        category=category,
                                                        image= image,
                                                        user=user,
                                                        )
            
            # Create a starting bid and assign it to created listing
            new_bid = AuctionBid.objects.create(price=price,
                                                auction=new_listing,
                                                user=user)
            
            return HttpResponseRedirect(reverse("index"))

        else:
            return render(request, "auctions/error.html",{
                "information": "Form is not valid"
            })
    else:
        form = AuctionListingForm()
        all_categories = AuctionCategory.objects.all()
        return render(request, "auctions/create_listing.html",{
            "form": form,
            "categories" : all_categories
        })

@login_required
def bid_listing(request, listing_id):
    if request.method=="POST":
        form = AuctionBidForm(request.POST)
        if form.is_valid():
            new_bid_value = form.cleaned_data["bid_amount"]
            curr_listing = AuctionListing.objects.get(id=listing_id)
            if new_bid_value > curr_listing.bids.all().last().price+1:
                AuctionBid.objects.create(price=new_bid_value,
                                        auction=curr_listing,
                                        user=request.user)
    return HttpResponseRedirect(reverse("listing_id", args=[curr_listing.id]))

@login_required
def delete(request, listing_id):
    user = request.user
    try:
        curr_listing = get_object_or_404(AuctionListing, pk=listing_id)
        curr_user_listings = user.auction_author.all()
        if curr_listing in curr_user_listings or user.is_superuser:
            curr_listing.delete()
        return HttpResponseRedirect(reverse("index"))
    
    except AuctionListing.DoesNotExist:
        return render(request, "auctions/error.html", {
            "information": "Listing not found"
        })
    

@login_required
def watchlist(request):
    user = request.user
    try:
        watch_list = user.watching_listing.all()
        if watch_list:
            return render(request, "auctions/watchlist.html",{
                "watchlist": watch_list
            })
        else:
            return render(request, "auctions/watchlist.html")
    
    # No such table -> no user has item in the watchlist
    except OperationalError:
        return render(request, "auctions/watchlist.html")


@login_required
def add_to_watchlist(request, listing_id):
    user = request.user
    try:
        curr_listing = get_object_or_404(AuctionListing, pk=listing_id)
        curr_listing.watch_list.add(user)
        return HttpResponseRedirect(reverse("index"))
    except AuctionListing.DoesNotExist:
        return render(request, "auctions/error.html",{
            "information": "Cannot add not exisiting item to watchlist"
        })

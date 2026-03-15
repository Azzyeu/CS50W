from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django import forms

from .models import User, Listing, Bid, Comment


def index(request):
    listings = Listing.objects.filter(is_active=True)
    return render(request, "auctions/index.html", {
        "listings": listings
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


class NewListingForm(forms.Form):
    title = forms.CharField(label="Title", required=True)
    description = forms.CharField(widget=forms.Textarea, required=True)
    price = forms.DecimalField(label="Price", required=True)
    category = forms.CharField(label="Category", required=False)
    image_url = forms.URLField(label="Image URL", required=False)

    def clean_image_url(self):
        image_url = self.cleaned_data.get("image_url")

        if not image_url:
            return Listing._meta.get_field("image_url").get_default()

        return image_url

class NewBidForm(forms.Form):
    bid = forms.DecimalField(label="Bid", required=True)


class NewCommentForm(forms.Form):
    comment = forms.CharField(label="Comment", widget=forms.Textarea, required=False)


@login_required
def create(request):
    if request.method == "POST":
        form = NewListingForm(request.POST)
        if form.is_valid():
            user = request.user
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            price = form.cleaned_data["price"]
            category = form.cleaned_data["category"]
            image_url = form.cleaned_data["image_url"]
            
            listing = Listing(user=user,
                              title=title, 
                              description=description, 
                              price=price, 
                              category=category, 
                              image_url=image_url)
            listing.save()

            return redirect(reverse("index"))
        
    else:
        form = NewListingForm()

    return render(request, "auctions/create.html", {
        "form": NewListingForm()
    })


def view_listing(request, title):
    listing = Listing.objects.get(title=title)
    is_watching = request.user in listing.watchlist.all()

    comments = Comment.objects.filter(listing=listing)
    clean_comments = [comment for comment in comments if comment]

    bid_form = NewBidForm()
    comment_form = NewCommentForm()
    valid_bid = True
    
    winner = None

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "comment":
            form = NewCommentForm(request.POST)

            if form.is_valid():
                user = request.user
                description = form.cleaned_data["comment"]

                comment = Comment(user=user,
                                listing=listing,
                                description=description)
                comment.save()

            return redirect(reverse("view_listing", args=[title]))

        if request.user != listing.user:
            if action == "bid":
                form = NewBidForm(request.POST)

                if form.is_valid():
                    user = request.user
                    amount = form.cleaned_data["bid"]

                    if amount <= listing.price:
                        valid_bid = False
                        return render(request, "auctions/listing.html", {
                            "listing": listing,
                            "bid_form": bid_form,
                            "comment_form": comment_form,
                            "is_watching": is_watching,
                            "valid_bid": valid_bid,
                            "comments": clean_comments,
                            "winner": winner
                        })

                    bid = Bid(user=user,
                            listing=listing,
                            amount=amount)
                    bid.save()

                    listing.price = amount
                    listing.save()

                    return redirect(reverse("view_listing", args=[title]))
            
            elif action == "toggle_watchlist":
                if is_watching:
                    listing.watchlist.remove(request.user)
                else:
                    listing.watchlist.add(request.user)

                return redirect(reverse("view_listing", args=[title]))
            
        else:
            if action == "close_listing":
                listing.is_active = False
                listing.save()

            return redirect(reverse("view_listing", args=[title]))
    
    if not listing.is_active:
        winner = listing.bids.order_by("-amount").first().user

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "bid_form": bid_form,
        "comment_form": comment_form,
        "is_watching": is_watching,
        "valid_bid": valid_bid,
        "comments": clean_comments,
        "winner": winner
    })


@login_required
def watchlist(request):
    watchlist = request.user.watchlist.all()
    return render(request, "auctions/watchlist.html", {
        "watchlist": watchlist
    })

def list_categories(request):
    categories = Listing.objects.values_list("category", flat=True).distinct()
    clean_categories = [category for category in categories if category]
    return render(request, "auctions/list_categories.html", {
        "categories": clean_categories
    })

def category(request, category):
    listings = Listing.objects.filter(category=category)
    return render(request, "auctions/category.html", {
        "category": category,
        "listings": listings
    })
    
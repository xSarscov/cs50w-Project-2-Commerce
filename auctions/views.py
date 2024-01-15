from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from decimal import Decimal, InvalidOperation

from .models import User, Listing, Category, Bid, Watchlist, Comments
from .forms import CreateListingForm, CreateBidForm, CommentsForm


def index(request):
    listings = Listing.objects.filter(is_active=True)
    return render(request, "auctions/index.html", {
        "listings": listings
    })


# Listing CRUD
@login_required
def create_listing(request):
    if request.method == 'POST':
        form = CreateListingForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            image = form.cleaned_data['image']
            category_id = form.cleaned_data['category']
            price = form.cleaned_data['price']

            category = Category.objects.get(id=category_id)

            new_listing = Listing(title=title, description=description, image=image, category=category, price=price, user=request.user)

            new_listing.save()

            return redirect('index')
        else:
            return render(request, "auctions/create_listing.html", {
                "form": form
            })
            

    form = CreateListingForm()
    return render(request, "auctions/create_listing.html", {
        'form': form
    })

@login_required
def listing_details(request, listing_id):

    listing, best_bid, total_bids, form, in_watchlist, comments, total_comments = get_listing_details(listing_id, request.user)
    comment_form = CommentsForm()
    error = None
    winner = Bid.objects.filter(listing=listing, is_winner=True).first()


    if request.method == 'POST':
        form = CreateBidForm(request.POST)

        if form.is_valid():
            bid = form.cleaned_data['bid']

            try:
                bid = Decimal(bid)

                if best_bid and bid > best_bid.amount and bid > listing.price or bid > listing.price:
                    offer = Bid(amount=bid, listing=listing, user=request.user)
                    offer.save()
                    return redirect('listing_details', listing_id=listing_id)
                else:
                    error = "The price you entered must be greater than the last bid"

            except InvalidOperation:
                error = "The price you entered is invalid."

    else:
        form = CreateBidForm()

    context = {
        "listing": listing,
        "best_bid": best_bid,
        "total_bids": total_bids,
        "form": form,
        "in_watchlist": in_watchlist,
        "comments": comments,
        "total_comments": total_comments,
        "error": error,
        "comment_form": comment_form,
        "winner": winner
    }

    return render(request, "auctions/listing_details.html", context)


@login_required
def add_comment(request, listing_id):
    if request.method == 'POST':
        comment_form = CommentsForm(request.POST)

        if comment_form.is_valid():
            content = comment_form.cleaned_data['comment']

            listing = get_object_or_404(Listing, pk=listing_id)
            comment = Comments(content=content, listing=listing, user=request.user)
            comment.save()
            return redirect('listing_details', listing_id=listing_id)
    
        listing, best_bid, total_bids, form, in_watchlist, comments, total_comments = get_listing_details(listing_id, request.user)
    
        context = {
            "listing": listing,
            "best_bid": best_bid,
            "total_bids": total_bids,
            "form": form,
            "in_watchlist": in_watchlist,
            "comments": comments,
            "total_comments": total_comments,
            "comment_form": comment_form
        }

    return render(request, "auctions/listing_details.html", context)

            
def get_listing_details(listing_id, user):
    listing = get_object_or_404(Listing, pk=listing_id)
    bids = Bid.objects.filter(listing=listing)
    best_bid = bids.order_by('-amount').first()
    total_bids = len(bids)
    form = CreateBidForm()
    in_watchlist = Watchlist.objects.filter(listing=listing, user=user).exists()
    comments = Comments.objects.filter(listing=listing)
    total_comments = len(comments)

    return listing, best_bid, total_bids, form, in_watchlist, comments, total_comments

@login_required
def watchlist(request):
    my_watchlist = Watchlist.objects.filter(user=request.user).first()

    return render(request, "auctions/watchlist.html", {
        "watchlist": my_watchlist,
    })

@login_required
def add_watchlist(request, listing_id):
    if request.method == 'POST':
        listing = get_object_or_404(Listing, pk=listing_id)
        watchlist, created = Watchlist.objects.get_or_create(user=request.user)            
        watchlist.listing.add(listing)

        request.session['watchlist_count'] = watchlist.listing.count()

        return redirect('listing_details', listing_id=listing_id)

@login_required
def remove_watchlist(request, listing_id):
    if request.method == 'POST':
        listing = get_object_or_404(Listing, pk=listing_id)
        watchlist = Watchlist.objects.get(listing=listing, user=request.user)
        watchlist.listing.remove(listing)

        request.session['watchlist_count'] = watchlist.listing.count()

        return redirect('listing_details', listing_id=listing_id)

@login_required
def close_auction(request, listing_id):
    if request.method == 'POST':
        listing = get_object_or_404(Listing, pk=listing_id)
        best_bid = Bid.objects.filter(listing=listing).order_by('-amount').first()
        
        if best_bid:
            Bid.objects.filter(listing=listing, amount=best_bid.amount).update(is_winner=True)

        listing.is_active = False
        listing.save()

        return redirect('listing_details', listing_id=listing_id)

@login_required
def open_auction(request, listing_id):
    if request.method == 'POST':
        listing = get_object_or_404(Listing, pk=listing_id)

        listing.is_active = True
        listing.save()

        return redirect('listing_details', listing_id=listing_id)
    
def categories(request):
    categories = Category.objects.all()
    return render(request, "auctions/categories.html", {
        "categories": categories
        })

def category_details(request, category_id):
    listings = Listing.objects.filter(category=category_id)
    return render(request, "auctions/category_details.html", {
        "listings": listings
    })

# Auth
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            watchlist = Watchlist.objects.filter(user=request.user).first()
            request.session['watchlist_count'] = watchlist.listing.all().count()


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

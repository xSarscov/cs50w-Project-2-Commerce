from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Listing, Category
from .forms import CreateListingForm


def index(request):
    listings = Listing.objects.filter(user=request.user)
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
            print(form.errors)
            return render(request, "auctions/create_listing.html", {
                "form": form
            })
            

    form = CreateListingForm()
    return render(request, "auctions/create_listing.html", {
        'form': form
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

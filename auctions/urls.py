from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("listing_details/<int:listing_id>", views.listing_details, name="listing_details"),
    path("add_comment/<int:listing_id>", views.add_comment, name="add_comment"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("add_watchlist/<int:listing_id>", views.add_watchlist, name="add_watchlist"),
    path("remove_watchlist/<int:listing_id>", views.remove_watchlist, name="remove_watchlist"),
    path("close_auction/<int:listing_id>", views.close_auction, name="close_auction"),
    path("open_auction/<int:listing_id>", views.open_auction, name="open_auction"),
    path("categories", views.categories, name="categories"),
    path("category_details/<int:category_id>", views.category_details, name="category_details"),
]

from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"), # index shows active listings
    path("create_listing", views.create_listing, name="create_listing"), 
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listing/<str:listing_id>", views.show_listing, name="show_listing"), 
    path("add_comment", views.add_comment, name="add_comment"), 
    path("add_to_watchlist", views.add_to_watchlist, name="add_to_watchlist"), 
    path("remove_from_watchlist", views.remove_from_watchlist, name="remove_from_watchlist"), 
    path("view_watchlist", views.view_watchlist, name='view_watchlist'), 
    path("view_all_listings", views.view_all_listings, name="view_all_listings"), 
    path("submit_bid", views.submit_bid, name="submit_bid"), 
    path("close_auction", views.close_auction, name="close_auction"), 
    path("view_categories", views.view_categories, name="view_categories"), 
    path("view_listing_given_category/<str:category>", views.view_listing_given_category, name="view_listing_given_category")
]


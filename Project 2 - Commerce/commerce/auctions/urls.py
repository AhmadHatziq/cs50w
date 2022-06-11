from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create_listing", views.create_listing, name="create_listing"), 
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listing/<str:listing_id>", views.show_listing, name="show_listing"), 
    path("add_comment", views.add_comment, name="add_comment"), 
    path("add_to_wishlist", views.add_to_wishlist, name="add_to_wishlist")
]

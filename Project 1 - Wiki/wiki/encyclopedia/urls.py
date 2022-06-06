from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"), 
    path("search", views.search, name="search"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("edit_page", views.edit_page, name="edit_page"), 
    path("random_page", views.random_page, name="random_page"), 
    path("<str:title>", views.display_entry, name="display_entry"), 
]

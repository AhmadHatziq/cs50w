from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"), 
    path("search", views.search, name="search"),
    path("<str:title>", views.display_entry, name="display_entry"), 
    
]

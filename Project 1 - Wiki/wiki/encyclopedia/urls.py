from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"), 
    path("search", views.search, name="search"),
    path("create_page", views.create_page, name="create_page"), 
    path("<str:title>", views.display_entry, name="display_entry"), 
    
]

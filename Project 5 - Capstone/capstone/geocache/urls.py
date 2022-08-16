from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"), 
    path("view_map", views.view_map, name="view_map"), 
    path("submit_geocache", views.submit_geocache, name="submit_geocache"), 
    path("discussion_board", views.discussion_board, name="discussion_board"), 
    path("geocache_discussion_post/<str:geocache_id>", views.geocache_discussion_post, name="geocache_discussion_post"),  
    path("test_geoposition", views.test_geoposition, name="test_geoposition"), 
    path("error", views.error, name="error")
]

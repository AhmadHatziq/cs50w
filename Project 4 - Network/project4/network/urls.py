
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"), 
    path("new_post", views.new_post, name="new_post"), 
    path("profile/<str:username>", views.display_user_profile, name="display_user_profile"), 
    path("follow", views.follow, name="follow"), 
    path("like", views.like, name="like"), 
    path("edit_post_via_POST", views.edit_post_via_POST, name="edit_post_via_POST"), 
    path("edit_post_via_AJAX", views.edit_post_via_AJAX, name="edit_post_via_AJAX"), 
    path("display_following_users", views.display_following_users, name="display_following_users")
    
]

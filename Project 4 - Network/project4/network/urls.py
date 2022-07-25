
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"), 
    path("new_post", views.new_post, name="new_post"), 
    path("profile/<str:username>", views.display_user_profile, name="display_user_profile")

]

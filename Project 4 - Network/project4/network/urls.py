
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"), 
    path("new_post", views.new_post, name="new_post"), 
    path("test_pagination", views.test_pagination, name="test_pagination")

]

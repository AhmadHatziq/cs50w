from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"), 
    path("main_map", views.main_map, name="main_map"), 
    path("test_geoposition", views.test_geoposition, name="test_geoposition")
]

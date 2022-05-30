from django.urls import path 
from . import views # Use '.' to import from the same directory

urlpatterns = [
    path("", views.index, name="index")
]


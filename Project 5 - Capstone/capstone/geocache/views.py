from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator 
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from . import utils
from .models import User 

from .models import PointOfInterest

API_KEY = utils.load_google_maps_API_key()

def index(request): 
    '''
    Index.html will get user coordinates and store it on the client-side. 
    '''
    return render(request, "geocache/index.html")

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "geocache/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "geocache/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "geocache/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user and followRelation 
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "geocache/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "geocache/register.html")

def view_map(request): 
    '''
    Renders the map as well as geocaches (solved and not solved). 
    '''
    context_dict = {
        'API_KEY': API_KEY
    }

    return render(request, 'geocache/main_map.html', context_dict)

def test_geoposition(request):
    '''
    Code taken from https://github.com/philippbosch/django-geoposition/blob/master/example/templates/poi_list.html
    '''
    pois = PointOfInterest.objects.all()
    return render(request, 'geocache/test_geoposition.html', 
    {
        'pois': pois, 'API_KEY': API_KEY
        }
        )







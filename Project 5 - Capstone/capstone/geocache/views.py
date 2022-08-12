from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator 
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from . import utils
from .models import User, Geocache, DiscussionBoard 


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

    # Checks if banner message exists and add it to the context dict if so. 
    if 'banner_message' in request.session: 
        banner_message = request.session['banner_message']
        del request.session['banner_message']
        context_dict['message'] = banner_message

    return render(request, 'geocache/main_map.html', context_dict)

def submit_geocache(request): 
    '''
    Handles the event where the user either wants to get the form to submit a new geocache (GET) or 
    is POSTING data from a geocache form. 
    '''

    # Returns the form to the user. 
    if request.method == "GET":
        context_dict = {
            'API_KEY': API_KEY
        }
        
        return render(request, 'geocache/submit_geocache.html', context_dict)

    # Process form info sent to the server. 
    if request.method == "POST": 

        # Extract parameters. 
        latitude = request.POST['latitude']
        longitude = request.POST['longitude']
        geocache_text_hint = request.POST['geocache_text_hint']
        poster = request.user.username 

        # Store into the DB. 
        user_object = User.objects.get(username = poster)
        new_geocache_post = Geocache(
            latitude = float(latitude), 
            longitude = float(longitude), 
            hint = geocache_text_hint, 
            isFound = False, 
            poster = User.objects.get(username = poster), 
        )
        new_geocache_post.save()
        print(f'Saved new geocache into GEOCACHE: {new_geocache_post}')

        # Redirect to map with message that the geocache has been saved. 
        request.session['banner_message'] = 'Geocache successfully saved. Please see it in the map below.'
        return HttpResponseRedirect(reverse("view_map"))


    return render(request, 'geocache/error.html')



    

def test_geoposition(request):
    '''
    Code taken from https://github.com/philippbosch/django-geoposition/blob/master/example/templates/poi_list.html
    Used for testing. 
    '''
    # pois = PointOfInterest.objects.all()
    return render(request, 'geocache/test_geoposition.html', 
    {
        'pois': pois, 'API_KEY': API_KEY
        }
        )

def error(request): 
    '''
    Returns an error page. Used for testing. 
    '''
    return render(request, 'geocache/error.html')




from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator 
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from . import utils
from .models import User, Geocache, DiscussionBoard 

import json

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

def process_geocache(request): 
    '''
    Extracts the Geocache data from the DB and processes it according to the current user. 
    Returns a list of processed Geocaches. 
    '''
    # Extract the geocache data out. 
    goecache_posts = Geocache.objects.all() 
    current_user = User.objects.get(username=request.user.username)

    # Process the geocache posts and check if: 
    #   (i)     the current user is the owner (user pin will show a different color)
    #   (ii)    that post has been found yet by the user
    processed_geoposts = []
    for geocache_post in goecache_posts: 

        # Check if the user logged in is the poster of this particular post. 
        is_owner = False
        if geocache_post.poster == current_user: 
            is_owner = True 

        # Check if the current user has found the geocache. Owners cannot find their own geocaches. 
        is_founder = False 
        founders = geocache_post.founder.all() 
        if current_user in founders: 
            is_founder = True 

        # Determine which icon to use based on is_owner and is_founder. 
        # Icon used is based on category. 
        geocache_category = ''
        STATIC_ICON_DIRECTORY = r'/static/geocache/images/'
        OWNER_ICON, UNFOUND_ICON, FOUND_ICON = 'blue_map_icon.png', 'blue_map_icon.png', 'red_map_icon.png' 
        icon_location = ''
        if is_owner: 
            icon_location = STATIC_ICON_DIRECTORY + OWNER_ICON
            geocache_category = 'created'
        else: 
            if is_founder: 
                icon_location = STATIC_ICON_DIRECTORY + FOUND_ICON 
                geocache_category = 'discovered'
            else: 
                icon_location = STATIC_ICON_DIRECTORY + UNFOUND_ICON
                geocache_category = 'undiscovered'

        # Check if the current user has added this geocache to their watchlist. 
        in_watchlist = False
        watchlist_users = geocache_post.users_following.all() 
        if current_user in watchlist_users: 
            in_watchlist = True 

        # Store fields in a new dictionary and append to the list 
        single_geocache = {
            'is_owner': str(is_owner), 
            'is_founder': str(is_founder), 
            'in_watchlist': str(in_watchlist),
            'icon_location': icon_location,
            'latitude': str(geocache_post.latitude), 
            'longitude': str(geocache_post.longitude), 
            'hint': geocache_post.hint, 
            'title': geocache_post.title, 
            'poster': str(geocache_post.poster), 
            'timestamp': str(geocache_post.timestamp.isoformat()), 
            'num_users_solved': len(geocache_post.founder.all()), 
            'DISCUSSION_BOARD_PLACEHOLDER': 'DISCUSSION_BOARD_PLACEHOLDER', 
            'geocache_category': geocache_category, 
            'id': str(geocache_post.id)
        }
        processed_geoposts.append(single_geocache)
    
    return processed_geoposts 

def view_map(request): 
    '''
    Renders the map as well as geocaches (solved and not solved). 
    '''

    # Extracts the Google maps API key out. 
    context_dict = {
        'API_KEY': API_KEY
    }

    # Checks if banner message exists and add it to the context dict if so. 
    # Used when redirecting after user has submitted a geocache. 
    if 'banner_message' in request.session: 
        banner_message = request.session['banner_message']
        del request.session['banner_message']
        context_dict['message'] = banner_message

    # Extract the geocache data out. 
    goecache_posts = Geocache.objects.all() 
    current_user = User.objects.get(username=request.user.username)

    # Process the geocache posts and check if: 
    #   (i)     the current user is the owner (user pin will show a different color)
    #   (ii)    that post has been found yet by the user
    processed_geoposts = process_geocache(request)
    
    # Add processed geoposts to context dictionary. 
    # Convert to json dumps so that JavaScript can recreate the object. 
    # We use the json library as in JavaScript, strings have double quotes. 
    # But in Python, it can be single quotes (which messes up JavaScript's JSON parser). 
    # Taken from https://stackoverflow.com/questions/4162642/single-vs-double-quotes-in-json

    context_dict['geocaches'] = json.dumps(processed_geoposts)

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
        geocache_title = request.POST['geocache_title']

        # Store into the DB. 
        new_geocache_post = Geocache(
            latitude = float(latitude), 
            longitude = float(longitude), 
            hint = geocache_text_hint, 
            title = geocache_title,
            isFound = False, 
            poster = User.objects.get(username = poster), 
        )
        new_geocache_post.save()
        print(f'Saved new geocache into GEOCACHE: {new_geocache_post}')

        # Redirect to map with message that the geocache has been saved. 
        request.session['banner_message'] = 'Geocache successfully saved. Please see it in the map below.'
        return HttpResponseRedirect(reverse("view_map"))


    return render(request, 'geocache/error.html')

def discussion_board(request): 
    '''
    Renders the discussion board, which displays details about all the geocaches, categorized into the 3 categories (Undiscovered, Discovered, Created)

    '''

    # Extract and process the geocache data. 
    processed_geocaches = process_geocache(request)

    # Filter the geocache data according to the 3 categories. 
    undiscovered_geocaches, discovered_geocaches, created_geocaches = [], [], []
    for geocache in processed_geocaches: 
        geocache_category = geocache['category']

        if geocache_category == 'created': 
            created_geocaches.append(geocache) 
        elif geocache_category == 'discovered': 
            discovered_geocaches.append(geocache)
        elif geocache_category == 'undiscovered': 
            undiscovered_geocaches.append(geocache)

    context_dict = {
        'undiscovered_geocaches_list': undiscovered_geocaches, 
        'discovered_geocaches_list': discovered_geocaches, 
        'created_geocaches_list': created_geocaches
    }

    return render(request, 'geocache/discussion_board.html', context_dict)

def test_geoposition(request):
    '''
    Code taken from https://github.com/philippbosch/django-geoposition/blob/master/example/templates/poi_list.html
    Used for testing. 
    '''
    # pois = PointOfInterest.objects.all()
    return render(request, 'geocache/test_geoposition.html', 
    {
        'API_KEY': API_KEY
    })

def error(request): 
    '''
    Returns an error page. Used for testing. 
    '''
    return render(request, 'geocache/error.html')




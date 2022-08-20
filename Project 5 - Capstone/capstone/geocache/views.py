from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator 
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms 

from . import utils
from .models import User, Geocache, DiscussionBoard 

import json

API_KEY = utils.load_google_maps_API_key()

class CommentForm(forms.Form): 
    comment_text = forms.CharField() 
    image_file = forms.ImageField()

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
    Helper function for view_map(...) and submit_geocache(...). 
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

        # Assigns a category & determines which icon to use based on is_owner and is_founder. 
        # Icon used is based on category. 
        geocache_category = ''
        STATIC_ICON_DIRECTORY = r'/static/geocache/images/'
        OWNER_ICON, UNFOUND_ICON, FOUND_ICON = 'blue_map_icon.png', 'green_map_icon.png', 'red_map_icon.png' 
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
            'category': geocache_category, 
            'id': str(geocache_post.id)
        }
        processed_geoposts.append(single_geocache)
    
    return processed_geoposts 

def view_map(request): 
    '''
    Renders the map as well as geocaches (solved and not solved). 
    GET request is to get the map, PUT request is to update the state (if the user has solved the Geocache or not). 
    '''

    if request.method == 'PUT': 
        
        # Extract data out. 
        data = json.loads(request.body)
        print('Data sent via PUT to /view_map: ', data)
        user = data['user']
        status_to_set_to = data['status_to_set_to']
        geocache_id = data['geocache_id']

        # Query database and get models for current state. 
        user_object = User.objects.get(username=user)
        geocache_object = Geocache.objects.get(id = int(geocache_id))
        users_that_have_found_geocache = geocache_object.founder.all()

        # Set to different states according to argument. 
        if status_to_set_to == 'found': 
            
            # Check if the current user is in the list of found users. If not, add the user in. 
            if user_object not in users_that_have_found_geocache: 
                geocache_object.founder.add(user_object)

            print('Added {} to found_users for geocache id {}'.format(user, geocache_id))

        elif status_to_set_to == 'not_found': 

            # Check if the current user is in the list of found users. If so, remove the user. 
            if user_object in users_that_have_found_geocache: 
                geocache_object.founder.remove(user_object)

            print('Removed {} from found_users for geocache id {}'.format(user, geocache_id))

        print('List of founders for geocache {}: {}'.format(geocache_id, geocache_object.founder.all()))
        return HttpResponse(status=204)

    elif request.method == 'GET': 

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
        context_dict['logged_in_user'] = str(request.user.username); 

        return render(request, 'geocache/main_map.html', context_dict)

    # Request should be either of type GET or PUT. 
    return error(request)

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

    # Process form info sent to the server. Creates the Geocache and first post for the Discussion Board. 
    if request.method == "POST": 

        # Extract parameters. 
        latitude = request.POST['latitude']
        longitude = request.POST['longitude']
        geocache_text_hint = request.POST['geocache_text_hint']
        poster = request.user.username 
        geocache_title = request.POST['geocache_title']

        # Store into the Geocache DB. 
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

        # Store into the Discussion Board DB. 
        new_discussionboard_post = DiscussionBoard(
            geocache = new_geocache_post, 
            comment_poster = User.objects.get(username = poster), 
            comment_text = "Hi guys, I created a geocache called: " + geocache_title + ".\nThe hint is: " + geocache_text_hint
        )
        new_discussionboard_post.save() 
        print(f'Saved new discussionboard post into DiscussionBoard: {new_discussionboard_post}')

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

    # Filter the geocache data according to the 3 categories. Also extract the latest discussion board post for each geocache. 
    undiscovered_geocaches, discovered_geocaches, created_geocaches = [], [], []
    for geocache in processed_geocaches: 
        geocache_category = geocache['category']
        geocache_id = int(geocache['id'])

        # Extract latest discussion board post and add it into the dictionary. 
        geocache_object = Geocache.objects.get(id=geocache_id)
        latest_geocache_boardpost = DiscussionBoard.objects.filter(geocache = geocache_object).latest('timestamp')
        new_geocache_dict = geocache.copy() 
        new_geocache_dict['latest_post_text'] = str(latest_geocache_boardpost.comment_text)
        new_geocache_dict['latest_post_poster'] = str(latest_geocache_boardpost.comment_poster)

        # Parse datetime string
        timestamp_string = str(latest_geocache_boardpost.timestamp)
        date = timestamp_string.split(' ')[0]
        year = date.split('-')[0]
        month = date.split('-')[1]
        day = date.split('-')[2]
        time = timestamp_string.split(' ')[1]
        hour = time.split(':')[0]
        min = time.split(':')[1]
        new_geocache_dict['latest_post_datetime'] = "{}/{}/{} at {}:{}".format(day, month, year, hour, min)

        # Extract count of posts associated with geocache 
        new_geocache_dict['count_of_posts'] = len(DiscussionBoard.objects.filter(geocache = geocache_object))

        if geocache_category == 'created': 
            created_geocaches.append(new_geocache_dict) 
        elif geocache_category == 'discovered': 
            discovered_geocaches.append(new_geocache_dict)
        elif geocache_category == 'undiscovered': 
            undiscovered_geocaches.append(new_geocache_dict)

    context_dict = {
        'undiscovered_geocaches_list': undiscovered_geocaches, 
        'discovered_geocaches_list': discovered_geocaches, 
        'created_geocaches_list': created_geocaches
    }

    return render(request, 'geocache/discussion_board.html', context_dict)

def geocache_discussion_post(request, geocache_id): 
    '''
    Returns a page containing all discussion board posts regarding the geocache if request is GET. 
    Process comment form info if request is POST. 
    '''
    context_dict = {}

    # Process comment form information if GET. Then, display the comments back but with a banner message to inform that the comment is sent. 
    if request.method == "POST":
        context_dict['message'] = 'Comment successfully entered.'

        # Access parameters from the form. Comment text is compulsory but not images. 
        poster = request.POST['comment_poster']
        geocache_id = request.POST['geocache_id']
        comment_text = request.POST['comment_text']
        image_file = None
        if len(request.FILES) > 0: 
            image_file = request.FILES['image_file']
        
        # Save data into database Model. 
        geocache_object = Geocache.objects.get(id = int(geocache_id))
        user_object = User.objects.get(username = poster)
        discussion_board_object = DiscussionBoard(
            geocache = geocache_object, 
            comment_poster = user_object, 
            comment_text = comment_text, 
            comment_image = image_file
        )
        discussion_board_object.save()
        print(f'Saved new discussionboard post into DiscussionBoard: {discussion_board_object}')
        # Proceed with re-rendering the comment page. 

        
    # Extract out Geocache and DiscussionBoard posts 
    geocache_object = None
    try:
        geocache_object = Geocache.objects.get(id = int(geocache_id))
    except Geocache.DoesNotExist:
        return error(request)
    
    discussion_board_posts = DiscussionBoard.objects.filter(geocache = geocache_object)

    # Format API string to generate maps image. 
    image_string = ("https://maps.googleapis.com/maps/api/staticmap?zoom=18&size=600x300&maptype={}"
                    "&markers=color:red%7Clabel:X%7C{},{}&key={}").format("roadmap", geocache_object.latitude, geocache_object.longitude, API_KEY)
    image_template_string_prefix = "https://maps.googleapis.com/maps/api/staticmap?zoom=18&size=600x300&maptype=" 
    image_template_string_suffix = "&markers=color:red%7Clabel:X%7C{},{}&key={}".format(geocache_object.latitude, geocache_object.longitude, API_KEY)
    
    # Store Geocache object, image URLs and DiscussionBoard posts
    context_dict['geocache'] = geocache_object
    context_dict['geocache_image_url'] = image_string
    context_dict['image_template_string_prefix'] = json.dumps(image_template_string_prefix)
    context_dict['image_template_string_suffix'] = json.dumps(image_template_string_suffix)
    context_dict['discussion_board_posts'] = discussion_board_posts
    context_dict['comment_poster'] = request.user.username
    
    return render(request, 'geocache/geocache_discussion_post.html', context_dict)


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




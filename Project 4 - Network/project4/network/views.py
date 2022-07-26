from datetime import datetime

from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator 
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

import json 

from .models import User, Post, FollowRelation, Like

def index(request):

    # Processes all posts in the DB for pagination. 
    context_dict = get_paginated_posts(request)

    # Check if the session object has a banner message. 
    # If so, extract and remove it. And send it to index.html inside the context.  
    if 'banner_message' in request.session:
        banner_message = request.session['banner_message']
        del request.session['banner_message']

        context_dict['message'] = 'Your post was submitted successfully.'
        return render(request, "network/index.html", context_dict)

    return render(request, "network/index.html", context_dict)


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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user and followRelation 
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            followRelation = FollowRelation(follower=user)
            followRelation.save() 
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

def new_post(request): 
    '''
    Called when the post form is submitted. 
    Aims to store the new post data to the database and returns the user back to the index route. 
    Also creates a Like object for the new post, with no users inside. 
    '''
    if request.method == "POST":
    
        # Extract posted content and current username. 
        post_content = request.POST["post"]
        username = request.user.username

        # Log down content and username
        # print('\nUser submitted a new post.')
        # print(f'User: {username}')
        # print(f'Content: {post_content}\n')

        # Create new POST object and save to database. 
        new_post = Post(
            post_text_content = post_content, 
            post_user = User.objects.get(username = username)
        )

        new_post.save()
        print(f'[{datetime.now()}] - /new_post: New post created with contents: {new_post}')

        # Create new Like object and save to DB. 
        new_like = Like(
            liked_post = new_post
        )
        new_like.save() 
        print(f'[{datetime.now()}] - /new_post: New like created with contents: {new_like}')

        # Set session variable for banner_message and redirect to index.html 
        request.session['banner_message'] = 'Your post was submitted successfully.'
        source_address = (request.META.get('HTTP_REFERER'))
        return HttpResponseRedirect(source_address)

    else: 
        return render(request, "network/index.html")

def test_pagination(request):    
    '''
    Test out the pagination in Django, before integrating it into index.html. 
    '''
    
    # Extract all social media posts. 
    social_media_posts = Post.objects.all()

    # Set pagination to display to 5 per page 
    paginator = Paginator(social_media_posts, 5)
    
    # Extract out page_obg and generate page_range 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    page_range = list(paginator.page_range)
    context_dict = {
        'page_obj' : page_obj, 
        'page_range': page_range 
    }
    return render(request, 'network/paginator_test.html', context_dict)

def get_paginated_posts(request): 
    '''
    Helper function to obtain media post as a pagination dictionary. 
    Returns a context dictionary to be passed to the template. 
    '''

    # Extract all social media posts. Sort to let the latest one appear first.  
    social_media_posts = Post.objects.all().order_by('-post_timestamp__hour', '-post_timestamp__minute', '-post_timestamp__second')

    # Set pagination to display to 10 per page 
    paginator = Paginator(social_media_posts, 10)
    
    # Extract out page_obg and generate page_range 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    page_range = list(paginator.page_range)
    context_dict = {
        'page_obj' : page_obj, 
        'page_range': page_range 
    }

    return context_dict 

def display_user_profile(request, username): 
    '''
    Displays the user profile given the username. 
    Uses the 'user_profile.html' template file. 
    '''

    # Checks if the username is valid. If so, shows the posts made by that user. 
    try:
        
        # Extract user information
        user_profile_object = User.objects.get(username=username)
        user_email = user_profile_object.email 
        user_join_date = user_profile_object.date_joined.date() 
        
        # Only allow un/follow button if user is logged in and not the profile user. 
        # Also checks that if the user is logged on, determine if the user is currently following the user profile. 
        allow_follow_button, currently_following = False, False
        if request.user.is_authenticated:
            current_username = request.user.username
            current_user_object = User.objects.get(username=current_username)
            if current_username != username:
                allow_follow_button = True 
            
            # Queries and gets the current followers that the current user is following 
            followRelation = FollowRelation.objects.get(follower=current_user_object) 
            users_currently_following = followRelation.users_following.all()
            if user_profile_object in users_currently_following: 
                currently_following = True 

        # Extract posts, sort by time. 
        posts_made_by_user = Post.objects.filter(post_user = user_profile_object)
        posts_made_by_user = posts_made_by_user.order_by('-post_timestamp__hour', '-post_timestamp__minute', '-post_timestamp__second')
        
        # Extract follower count for user profile. 
        # Iterate through all users and increment count if they are following the user profile. 
        # Very inefficent due to data model. 
        all_users = User.objects.all()
        follower_count = 0 
        for user in all_users: 
            user_follow_relation = FollowRelation.objects.get(follower=user)
            if user_profile_object in user_follow_relation.users_following.all(): 
                follower_count+= 1 
                # print(f'{user.username} is following {user_profile_object.username}')
        # print('Follower count:', follower_count)

        # Extract following count for user profile. 
        user_profile_follow_relation = FollowRelation.objects.get(follower=user_profile_object)
        following_count = len(user_profile_follow_relation.users_following.all())

        # Pass parameters in context dictionary and render template. 
        context_dict = {
            'user_email': user_email, 
            'user_join_date': user_join_date, 
            'username': username, 
            'posts': posts_made_by_user, 
            'post_count': len(posts_made_by_user), 
            'allow_follow_button': allow_follow_button, 
            'currently_following': currently_following, 
            'follower_count': follower_count, 
            'following_count': following_count 
        }
        return render(request, "network/user_profile.html", context_dict)
    except User.DoesNotExist:
        error_message = f"The user you are looking for ('{username}') does not exist."
        return render(request, "network/user_profile.html", {"error_message": error_message})

def follow(request): 
    '''
    Handles when a user wants to follow or unfollow. 
    Is called via POST using asynchronous JavaScript. 
    '''
    if request.method == "POST": 

        # Extract parameters sent from JSON body. 
        data = json.loads(request.body)
        print(f'[{datetime.now()}] JSON body object received in /follow:', data)
        current_user = data['current_user']
        target_user = data['target_user']
        current_follow_status = (str(data['current_follow_status'])).lower()
        # print(current_follow_status)

        # Extract user objects from database. 
        current_user_object = User.objects.get(username=current_user)
        target_user_object = User.objects.get(username=target_user)

        # Extract the followRelation 
        followRelation = FollowRelation.objects.get(follower=current_user_object)

        # Update depending on current_follow_status 
        if current_follow_status in ['true', 'True']:
            # As user is already following the target, will proceed to unfollow.
            if target_user_object in followRelation.users_following.all(): 
                followRelation.users_following.remove(target_user_object) 
                print(f'[{datetime.now()}] - /follow: {current_user_object.username} has unfollowed {target_user_object.username}')
                return HttpResponse(status=204)
             
        elif current_follow_status in ['false', 'False']:  
            # As user is not following the target, will proceed to add the follow-relation.
            followRelation.users_following.add(target_user_object) 
            print(f'[{datetime.now()}] - /follow: {current_user_object.username} has followed {target_user_object.username}')
            return HttpResponse(status=204)
        else: 
            print(f'[{datetime.now()}] - /follow: Internal server error.')
            return HttpResponse(status=500)

    print(f'[{datetime.now()}] - /follow: Internal server error.')
    return HttpResponse(status=500)


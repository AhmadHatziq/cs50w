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

        context_dict['message'] = banner_message
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
    social_media_posts = Post.objects.all().order_by('-post_timestamp')

    # Extract the current user (if logged in)
    # If not logged in, username will be '' ie an empty string of length 0. 
    username = request.user.username

    # Process social media posts and attach 'like' button for each post. 
    processed_posts = []
    for post in social_media_posts:  

        # Extract out contents from QuerySet. 
        single_post_processed = {
            'post_text_content': post.post_text_content, 
            'post_user': post.post_user, 
            'post_timestamp': post.post_timestamp, 
            'post_id': post.id
        }

        # Extract Like parameters 
        like_object = Like.objects.get(liked_post=post)
        like_count = len(like_object.liked_by_users.all())
        like_id = like_object.id

        single_post_processed['like_count'] = like_count 
        single_post_processed['like_id'] = like_id 

        # Check if the currently logged in user has liked the post. 
        # Check if the current user is the post owner. 
        isUserLoggedIn = False
        hasUserLikedPost = False
        isPostOwner = False
        if len(username) > 0:  
            isUserLoggedIn = True 
            user_object = User.objects.get(username=username) 
            
            if user_object in like_object.liked_by_users.all(): 
                hasUserLikedPost = True 

            if username == post.post_user.username: 
                isPostOwner = True 
        
        single_post_processed['isUserLoggedIn'] = isUserLoggedIn
        single_post_processed['hasUserLikedPost'] = hasUserLikedPost
        single_post_processed['isPostOwner'] = isPostOwner
        
        # Append single post dictionary to the list. 
        processed_posts.append(single_post_processed)

    # Set pagination to display to 10 per page. Input to Paginator is a list. 
    paginator = Paginator(processed_posts, 10)
    
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

def like(request): 
    '''
    Handles when a user likes a post. 
    Is called via POST using asynchronous JavaScript. 
    '''
    if request.method == 'POST': 
        
        # Extract parameters from JSON body. 
        data = json.loads(request.body)
        print(f'[{datetime.now()}] JSON body object received in /like:', data)
        current_user = data['current_user']
        post_id = data['post_id']
        target_like_id = data['like_id']
        desired_end_state = data['desired_end_state'] 

        # Extract from models 
        user_object = User.objects.get(username=current_user)
        like_object = Like.objects.get(id=target_like_id) 

        # Process API request and set to like/unlike
        if desired_end_state == 'like': 

            # Add the user to the group that liked this post, if not done so. 
            if user_object not in like_object.liked_by_users.all():  
                like_object.liked_by_users.add(user_object)
            print(f'[{datetime.now()}] - /like - LIKE: {current_user} liked post #{post_id} with like ID #{target_like_id}')
            return HttpResponse(status=204)
        
        elif desired_end_state == 'unlike': 
            
            # Remove the user from the users that liked this post, if present. 
            if user_object in like_object.liked_by_users.all(): 
                like_object.liked_by_users.remove(user_object)
            print(f'[{datetime.now()}] - /like - UNLIKE: {current_user} unliked post #{post_id} with like ID #{target_like_id}')
            return HttpResponse(status=204)
        else: 
            return HttpResponse(status=500)

    return HttpResponse(status=500)

def edit_post_via_POST(request): 
    '''
    NOT USED as specs requires edits to be done asynchronously, not via POST and page reloads. 
    Route is used when the user wants to edit an existing post. 
    Data is sent via a form using POST. 
    '''
    if request.method == 'POST': 
        
        # Extract posted content and current username. 
        new_post_content = request.POST["new_post"]
        username = request.user.username
        post_id = request.POST['post_id']

        # Put edits into the DB. 
        post_to_edit = Post.objects.get(id=post_id)
        post_to_edit.post_text_content = new_post_content
        post_to_edit.save() 
        print(f"[{datetime.now()}] - /edit_post_via_POST - Updated post #{post_id}'s contents to {new_post_content}")

        # Return the user back to the index page.
        # With success message of edit changes to the post. 
        request.session['banner_message'] = 'Your post was edited successfully.'
        return HttpResponseRedirect(reverse("index"))
    pass

def edit_post_via_AJAX(request):
    '''
    Used to handle post edits. 
    Done via AJAX. 
    '''
    if request.method == 'POST': 
        
        # Extract parameters from JSON body. 
        data = json.loads(request.body)
        print(f'[{datetime.now()}] JSON body object received in /edit_post_via_AJAX:', data)
        post_id = data['post_id']
        new_post_content = data['new_post_content']

        # Update post content in the DB. 
        post_to_edit = Post.objects.get(id=post_id)
        post_to_edit.post_text_content = new_post_content
        post_to_edit.save() 
        print(f"[{datetime.now()}] - /edit_post_via_AJAX - Updated post #{post_id}'s contents to {new_post_content}")

        return HttpResponse(status=204)

def display_following_users(request): 
    '''
    Will display the posts from users that the current user is following. 
    '''

    # Get current user 
    current_user = request.user.username 
    current_user_object = User.objects.get(username=current_user)

    # Get user's FollowRelation object 
    current_follow_relation = FollowRelation.objects.get(follower=current_user_object)

    # Get users that the current user is following. 
    users_following = current_follow_relation.users_following.all() 

    # Get all posts from these users. 
    posts = [] 
    for user in users_following: 
        specific_user_posts = Post.objects.filter(post_user=user)
        for post in list(specific_user_posts): 
            posts.append(post)

    # Process each post. 
    processed_posts = []
    for post in posts: 
        
        single_post_processed = {
            'post_text_content': post.post_text_content, 
            'post_user': post.post_user, 
            'post_timestamp': post.post_timestamp, 
            'post_id': post.id
        }

        # Extract Like parameters 
        like_object = Like.objects.get(liked_post=post)
        like_count = len(like_object.liked_by_users.all())
        like_id = like_object.id

        single_post_processed['like_count'] = like_count 
        single_post_processed['like_id'] = like_id 

        # Check if the currently logged in user has liked the post. 
        # Check if the current user is the post owner. 
        isUserLoggedIn = True
        hasUserLikedPost = False
        isPostOwner = False

        current_user_object = User.objects.get(username=current_user) 

        if current_user_object in like_object.liked_by_users.all(): 
            hasUserLikedPost = True 

        if current_user == post.post_user.username: 
            isPostOwner = True 

        single_post_processed['isUserLoggedIn'] = isUserLoggedIn
        single_post_processed['hasUserLikedPost'] = hasUserLikedPost
        single_post_processed['isPostOwner'] = isPostOwner

        # Append single post dictionary to the list. 
        processed_posts.append(single_post_processed)

    # Set pagination to display to 10 per page. Input to Paginator is a list. 
    paginator = Paginator(processed_posts, 10)
    
    # Extract out page_obg and generate page_range 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    page_range = list(paginator.page_range)
    context_dict = {
        'page_obj' : page_obj, 
        'page_range': page_range, 
        'num_users_following': len(users_following), 
        'users_following': list(users_following)
    }

    # Render the following.html template
    return render(request, 'network/following.html', context_dict)
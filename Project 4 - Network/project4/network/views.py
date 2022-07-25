from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator 
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Post, FollowRelation, Like


def index(request):

    # Check if the session object has a banner message. 
    # If so, extract and remove it. And send it to index.html inside the context.  
    if 'banner_message' in request.session:
        banner_message = request.session['banner_message']
        del request.session['banner_message']

        context_dict = {'message': 'Your post was submitted successfully.'}
        return render(request, "network/index.html", context_dict)

    return render(request, "network/index.html")


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

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
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
        print(f"\nSaved new post into POST model: {new_post}\n")

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
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'network/paginator_test.html', {'page_obj' : page_obj})




    

def hardcode_make_b_follow_a(request):
    '''
    Test out adding a follower to a user as hard to do so via Admin GUI. 
    '''
    user_a = User.objects.get(username = 'a')
    user_b = User.objects.get(username = 'b')
    
    # If b follows a, need to 1) add user a to b's following list. 2) add user b to a's follower list. 
    user_b.following.add(user_a)
    user_a.followers.add(user_b)
    print('User B is now following User A')
    print('B is following: ', user_b.following.all())
    print('A followers: ', user_a.followers.all())

    return render(request, "network/index.html")

from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User


def index(request):
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

        print(f'User: {username}')
        print(f'Content: {post_content}')

        # Create a message to inform user that comment was sent successfully. 
        context_dict = {'message': 'Your post was submitted successfully.'}

        return render(request, "network/index.html", context_dict)
    else: 
        return render(request, "network/index.html")



    

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

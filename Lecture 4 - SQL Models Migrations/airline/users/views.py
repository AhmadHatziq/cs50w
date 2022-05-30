from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

# Create your views here.
def index(request): 

    # This are Django provided fields
    # If user is not authenticated, redirect to login page 
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    else: 
        # Redirect user to user.html to see his details 
        print(dir(request.user))
        print(request.user.password)
        return render(request, "users/user.html")
        
    
        
def login_view(request):

    # Handle the case where user login data is sent via POST. 
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        
        # Authentication is done by the Django provided functions. 
        # It will check if the credentials exist in the database. 
        user = authenticate(request, username=username, password=password) 
        if user is not None: # ie user credentials are valid
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else: 
            # Show an error message if credentials are invalid. 
            return render(request, "users/login.html", {
                "message": "Invalid Credentials"
            })

    # Return login.html if not accessed via POST ie via normal GET method. 
    return render(request, "users/login.html")
    
def logout_view(request): 
    
    # Logout the user 
    logout(request) 
    
    return render(request, "users/login.html", {
        "message": "Successfully logged out."
    })
    
    
    
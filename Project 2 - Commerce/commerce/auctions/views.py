from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms 

from .models import User

class CreateListingForm(forms.Form): 
    listing_name = forms.CharField(label="Listing name", widget=forms.TextInput(attrs={'class':'form-control'}))
    listing_start_price = forms.DecimalField(label="Starting price", max_digits=9, decimal_places=2, widget=forms.TextInput(attrs={'class':'form-control'}))
    listing_url = forms.URLField(label="Image URL", max_length=256, widget=forms.TextInput(attrs={'class':'form-control'}))
    listing_desc = forms.CharField(label="Details", widget=forms.Textarea(attrs={'name':'body', 'rows':'3', 'cols':'5', 'class':'form-control'}))

def index(request):
    return render(request, "auctions/index.html")


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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user. Only 3 fields are needed: username, email, password 
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def create_listing(request): 
    
    # Checks for user name. Redirects back to login if user is not logged in. 
    if request.user.is_authenticated == False: 
        return render(request, "auctions/index.html", {
            "message": "Please login"
        })
        
    # Returns form template if method is by GET 
    if request.method == "GET":
        return render(request, "auctions/create_listing.html", {
            "form": CreateListingForm()
            })
     
    # Handle data sent from the form 
    if request.method == "POST": 
        
        # Check if form is valid and process data 
        form = CreateListingForm(request.POST)
        if form.is_valid(): 
            
            # print(form.cleaned_data)
            
            # Extract data from form 
            listing_name = form.cleaned_data['listing_name']
            listing_start_price = form.cleaned_data['listing_start_price']
            listing_image_url = form.cleaned_data['listing_url']
            listing_desc = form.cleaned_data['listing_desc']
            
            
            
            
    
    # Return to index otherwise
    return render(request, "auctions/index.html")
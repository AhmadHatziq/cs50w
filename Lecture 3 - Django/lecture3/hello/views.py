from django.shortcuts import render
from django.http import HttpResponse 

# Create your views here.
# Argument is a HTTP request object
def index(request): 
    return render(request, "hello/index.html")
    
def hello_brian(request): 
    return HttpResponse("Hello Brian!")

# Define a function to return a HTTP response based on the argument string name 
def greet(request, name): 

    # Below is returning only a capitalized string as the HTML
    # return HttpResponse(f"Hello, {name.capitalize()}")
    
    # Below will return a templated HTML with the name argument inputted inside 
    # The context is a dictionary with a key value of name. 
    context_dict = {"name": name.capitalize()}
    return render(request, "hello/greet.html", context_dict)
    
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

def index(request): 
    return render(request, "geocache/index.html")


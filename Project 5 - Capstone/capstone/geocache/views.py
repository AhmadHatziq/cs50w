from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from . import utils

API_KEY = utils.load_google_maps_API_key()

def index(request): 
    return render(request, "geocache/index.html")


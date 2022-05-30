from django.shortcuts import render
from django.http import HttpResponse 

import datetime 

# Create your views here.
def index(request): 
    
    # Calculate if it is a new year
    now = datetime.datetime.now()
    isNewYear = False   
    if now.month == 1 and now.day == 1: 
        isNewYear = True 
       
    # Create context dictionary and pass into render HTML
    context_dict = {
        "isNewYear": isNewYear
    }
    return render(request, "newyear/index.html", context_dict)
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse 

from .models import Flight, Passenger 

# Create your views here.

def index(request): 
    context_dict = {
        "flights": Flight.objects.all()
    }
    return render(request, "flights/index.html", context_dict)
    
def flight(request, flight_id):

    # Get all flights matching the ID via Primary Key
    flight = Flight.objects.get(pk = flight_id)
    
    context_dict = {
        "flight": flight, 
        "passengers": flight.passengers.all(), # As passengers is a related name 
        "non_passengers": Passenger.objects.exclude(flights=flight).all()
        } 
    
    return render(request, "flights/flight.html", context_dict)
    
def book(request, flight_id): 

    # Handle the case where data is being sent in via a form 
    # Incoming parameters are the passenger ID. Flight ID is in the URL. 
    if request.method == 'POST': 
        
        # Get the flight to add the passenger on 
        flight = Flight.objects.get(pk=flight_id)
        
        # Get the passenger from the database. Cast to int  
        passenger = Passenger.objects.get(pk = int(request.POST['passenger']))
        
        # Add the passenger to that flight 
        passenger.flights.add(flight)
        
        # Redirect User back to view changes 
        return HttpResponseRedirect(reverse("flight", args=(flight_id,))) # Argument is flight_id. 
        
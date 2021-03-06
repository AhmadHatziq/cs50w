from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db.models import Max
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from django import forms 

from .models import User, Category, Auction, Bid, Comment 

import decimal

'''
    Defines the form used to create an auction listing. 
    Note that the category is hardcored on the HTML template itself as it generate dynamically. 
'''
class CreateListingForm(forms.Form): 
    
    # The form elements. 
    listing_name = forms.CharField(label="Listing name", widget=forms.TextInput(attrs={'class':'form-control'}))
    listing_start_price = forms.DecimalField(label="Starting price", max_digits=9, decimal_places=2, widget=forms.TextInput(attrs={'class':'form-control'}))
    listing_url = forms.URLField(label="Image URL", max_length=256, widget=forms.TextInput(attrs={'class':'form-control'}))
    listing_desc = forms.CharField(label="Details", widget=forms.Textarea(attrs={'name':'body', 'rows':'3', 'cols':'5', 'class':'form-control'}))

'''
    Helper function to return active listings along with top current bidders. 
'''
def append_top_bidder_to_active_listings():

    # Extract active listings 
    active_listings = Auction.objects.filter(item_is_active = True)
    
    # Extract current bid count and highest bid for current listings
    active_listings_and_bid = []
    for listing in active_listings: 
    
        # Get matching bids for the item 
        # Note that .get() returns 1 item. Else there will be an error 
        item_bids = Bid.objects.filter(bid_item = listing)
        
        # Get bid count 
        bid_count = len(item_bids)
        
        # Get highest bid 
        highest_bid_amount, highest_bid_record = 0, None 
        for bid_record in item_bids: 
            
            current_bid = bid_record.bid_amount
            if current_bid > highest_bid_amount: 
                highest_bid_amount = current_bid 
                highest_bid_record = bid_record
        
        # Store listing and max bid details into a new dictionary and append to the new list       
        listing_and_bid = {
            'item_id': listing.id, 
            'item_name': listing.item_name, 
            'item_image_url': listing.item_image_url, 
            'item_description': listing.item_description, 
            'item_owner': listing.item_owner, 
            'item_category': listing.item_category, 
            'item_starting_bid': listing.item_starting_bid, 
            'item_bid_count': bid_count, 
            'item_max_bid': highest_bid_record.bid_amount, 
            'item_current_highest_bidder': highest_bid_record.bid_bidder
        }
        active_listings_and_bid.append(listing_and_bid)
        
    return active_listings_and_bid
           
# Index view contains all active listings. 
# Inactive listings are omitted. 
def index(request):

    active_listings_and_bid = append_top_bidder_to_active_listings()
    
    return render(request, "auctions/index.html", {
            "listings": active_listings_and_bid
        })


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

@login_required(login_url='/login')   
def create_listing(request): 
    
    # Checks for user name. Redirects back to login if user is not logged in. 
    if request.user.is_authenticated == False: 
        return render(request, "auctions/index.html", {
            "message": "Please login"
        })
        
    # Returns form template if method is by GET 
    if request.method == "GET":
        categories = Category.objects.all()
        category_choices = [i.category for i in categories]   
        return render(request, "auctions/create_listing.html", {
            "form": CreateListingForm(), 
            "categories": category_choices
                })
     
    # Handle data sent from the form 
    if request.method == "POST": 
        
        # Check if form is valid and process data 
        form = CreateListingForm(request.POST)
        if form.is_valid(): 
            
            # Extract data from form 
            listing_name = form.cleaned_data['listing_name']
            listing_start_price = form.cleaned_data['listing_start_price']
            listing_image_url = form.cleaned_data['listing_url']
            listing_desc = form.cleaned_data['listing_desc']
            
            # Extract category chosen as handled differently from Django forms. 
            listing_category = request.POST['category']
              
            # If it is a new category, insert into CATEGORY table 
            existing_categories = [i.category for i in Category.objects.all()] 
            if listing_category not in existing_categories: 
                new_category = Category(category=listing_category)
                new_category.save()
                print(f'Saved new category into CATEGORY: {new_category}')
            
            # Extract other data from the user 
            username = request.user.username 
            
            # Insert the new listing into the Auction table  
            new_listing = Auction(
                    item_name = listing_name, 
                    item_category = Category.objects.get(category = listing_category), 
                    item_owner = User.objects.get(username = username), 
                    item_image_url = listing_image_url, 
                    item_starting_bid = listing_start_price, 
                    item_description = listing_desc, 
                    item_is_active = True 
                )
            new_listing.save()
            print(f'Saved new listing into AUCTION: {new_listing}')
            
            # Insert the corresponding bid into the BID table 
            new_bid = Bid(
                    bid_amount = listing_start_price, 
                    bid_item = new_listing, 
                    bid_bidder = User.objects.get(username = username)
                )
            new_bid.save()
            print(f'Saved new bid into BID: {new_bid}')

            # Return to index to view active listings 
            return HttpResponseRedirect(reverse("index"))
    
    # Return to index otherwise
    return HttpResponseRedirect(reverse("index"))

# Shows the listing for a single particular listing ID. 
@login_required(login_url='/login')    
def show_listing(request, listing_id): 
    
    ''' DEPRACATED
    # Get all listings and filter down to current listing ID. 
    active_listings_and_bid = append_top_bidder_to_active_listings()
    current_listing = None 
    for listing in active_listings_and_bid: 
        if int(listing['item_id']) == int(listing_id): 
            current_listing = listing 
    '''

    # Get current listing 
    current_listing = Auction.objects.get(id=listing_id)
            
    # Get bidding history regarding this listing ID 
    bidding_history = Bid.objects.filter(bid_item = Auction.objects.get(id=listing_id))

    # Get current top bidder. 
    # Used to create view for closed bids. 
    highest_bid, highest_bidder = -1.0, None 
    for bid in bidding_history: 
        if highest_bid < float(bid.bid_amount):
            highest_bid = float(bid.bid_amount)
            highest_bidder = bid.bid_bidder
    
    # Get comments regarding this listing ID 
    comment_history = Comment.objects.filter(comment_listing = Auction.objects.get(id=listing_id))

    # Get boolean variable if listing is in user watch list 
    user = User.objects.get(username = request.user.username)
    listing = Auction.objects.get(id = listing_id)
    all_watching_users = listing.users_watching.all()
    currently_watching = False
    if user in all_watching_users:
        currently_watching = True

    # Get boolean variable if current user is the item owner. 
    listing_owner = listing.item_owner
    is_owner = False 
    if listing_owner == user: 
        is_owner = True 
    # print('Is owner:', is_owner)

    # Get boolean variable if item can be closed ie if username is the owner and item is still active.  
    show_auction_close_button = False 
    if is_owner == True and listing.item_is_active == True: 
        show_auction_close_button = True 
    
    # Return error if ID does not exist 
    if current_listing is None: 
        return render(request, "auctions/index.html", {
            "message": 'Unable to find specified listing ID', 
            "listings": append_top_bidder_to_active_listings()
        })
        
    # Returns the display_listing template 
    return render(request, "auctions/display_listing.html", {
        "listing": current_listing, 
        "bidding_history": bidding_history, 
        "comment_history": comment_history, 
        "currently_watching": currently_watching, 
        "is_owner": is_owner, 
        "bidding_status": listing.item_is_active, 
        "show_auction_close_button": show_auction_close_button, 
        "highest_bid": highest_bid, 
        "highest_bidder": highest_bidder, 
        "is_winner": True if str(highest_bidder) == str(user) else False, 
        
    })

@login_required(login_url='/login')   
# Comment is sent via POST from the display_listing page    
def add_comment(request): 
    if request.method == "POST": 
    
        # Extract posted parameters 
        comment = request.POST["comment"]
        listing_id = request.POST["listing_id"]
        
        # Create new comment object and save into DB.  
        new_comment = Comment(
            comment_string = comment, 
            comment_user = User.objects.get(username = request.user.username), 
            comment_listing = Auction.objects.get(id = listing_id)
        )
        new_comment.save()
        print(f'Saved new comment into COMMENT: {new_comment}')
        
        # Redirect back to original page 
        source_address = (request.META.get('HTTP_REFERER')) #Eg http://127.0.0.1:8000/listing/8
        return HttpResponseRedirect(source_address)
       
    else: 
        # User should not be arriving at this page via GET. 
        render(request, "auctions/index.html", {
            "listings": append_top_bidder_to_active_listings(), 
            "message": 'Error in submitting comment. Please try again.'
        })

@login_required(login_url='/login')   
# Handles the event when the user clicks to add to wishlist.         
def add_to_watchlist(request): 
    
    if request.method == 'GET':

        # Get username of the user and the listing id 
        # Listing ID is obtained by parsing the HTTP REFERER which is: http://127.0.0.1:8000/listing/8 
        username = request.user.username 
        source_address = (request.META.get('HTTP_REFERER'))
        listing_id = (str(source_address)).split('/')[-1]

        # Add that item to that users wishlist. 
        current_user = User.objects.get(username=username)
        current_listing = Auction.objects.get(id=listing_id)
        current_listing.users_watching.add(current_user)
        print('Added user {} to watchlist for item: {}'.format(current_user, current_listing))
        print('Current watchlist: ', current_listing.users_watching.all())
        
        # Debug
        # result =  (Auction.objects.get(id=listing_id)).users_watching.all()
        # print(result)

        # Redirect back to listing page 
         #Eg http://127.0.0.1:8000/listing/8
        return HttpResponseRedirect(source_address)

@login_required(login_url='/login')   
# Handles the event when the user clicks to remove from wishlist.  
def remove_from_watchlist(request): 
    if request.method == 'GET': 

        # Get parameters 
        username = request.user.username 
        source_address = (request.META.get('HTTP_REFERER'))
        listing_id = (str(source_address)).split('/')[-1]

        # Query and remove if the user exists in the watchlist 
        current_user = User.objects.get(username=username)
        current_listing = Auction.objects.get(id=listing_id)
        all_watching_users = current_listing.users_watching.all()
        # print(current_listing.users_watching.all())
        if current_user in all_watching_users: 
            current_listing.users_watching.remove(current_user)
        
        # print(current_listing.users_watching.all())
        print('Removed user {} from watchlist for item: {}'.format(current_user, current_listing))
        print('Current watchlist: ', current_listing.users_watching.all())

        return HttpResponseRedirect(source_address)

@login_required(login_url='/login') 
# Views the watchlist for a specified user. Does not care if item is inactive. 
def view_watchlist(request): 
    if request.method == 'GET':

        # Get username 
        username = request.user.username
        this_user = User.objects.get(username=username)

        # Get all items and filter down to those that have this user in their watchlist 
        items_user_watching = Auction.objects.filter(users_watching = this_user)

        return render(request, "auctions/view_watchlist.html", {
            "listings": items_user_watching
        })
        
# Views all listings, irregardless of active or inactive status.     
def view_all_listings(request): 
    if request.method =='GET': 
        
        # Get all items in the databse. 
        items = Auction.objects.all()

        return render(request, "auctions/all_listings.html", {
            "listings": items
        }) 

@login_required(login_url='/login') 
def submit_bid(request): 
    if request.method == 'POST': 
        
        # Extract parameters 
        submitted_bid = float(request.POST['bid_amount'])
        source_address = (request.META.get('HTTP_REFERER'))
        listing_id = (str(source_address)).split('/')[-1]
        username = request.user.username

        # Get max bid using for loop and counts of bids inside. 
        # If there is only one bid, allowed bid is >= max bid. Else, allowed bid is only > max bid. 
        bidding_history = Bid.objects.filter(bid_item = Auction.objects.get(id=listing_id))
        bid_count = len(bidding_history)
        max_bid = -1 
        for bid in bidding_history: 
            if max_bid <= float(bid.bid_amount): 
                max_bid = float(bid.bid_amount)
        # print(max_bid)
        
        # Get max bid using aggrregate method
        max_bid = Bid.objects.filter(bid_item = Auction.objects.get(id=listing_id)).aggregate(Max('bid_amount'))
        max_bid = (float(max_bid['bid_amount__max']))

        # Get current listing
        current_listing = Auction.objects.get(id=listing_id)

        # Get bidding history regarding this listing ID 
        bidding_history = Bid.objects.filter(bid_item = Auction.objects.get(id=listing_id))
        
        # Get comments regarding this listing ID 
        comment_history = Comment.objects.filter(comment_listing = Auction.objects.get(id=listing_id))
        

        # Return error message to user if submitted_bid is <= max_bid or < max_bid if first bid.
        # Reobtains values needed for show_listing. 
        if ((bid_count == 1) and (submitted_bid < max_bid)) or ((bid_count > 1) and (submitted_bid <= max_bid)):

            # Returns the display_listing template with error message that bid submitted is too low. 
            error_message = 'Bid failed as needs to be higher than {}'.format(float(max_bid))
            return render(request, "auctions/display_listing.html", {
                "listing": current_listing, 
                "bidding_history": bidding_history, 
                "comment_history": comment_history, 
                "message": error_message
            })

        # Add bid to database 
        # print(decimal.Decimal(submitted_bid))
        new_bid = Bid(
                bid_amount = decimal.Decimal(submitted_bid), 
                bid_item = Auction.objects.get(id=listing_id), 
                bid_bidder = User.objects.get(username = username)
        )
        new_bid.save()
        print(f'Saved new bid into BID: {new_bid}')
        
        # Redirect
        return HttpResponseRedirect(source_address)
               
@login_required(login_url='/login') 
def close_auction(request):
    # The button is only clickable by the item owner from the display_listing webpage

    # Extract information 
    source_address = (request.META.get('HTTP_REFERER'))
    listing_id = (str(source_address)).split('/')[-1]
    username = request.user.username

    # Mark item as closed 
    bid_item = Auction.objects.get(id=listing_id)
    bid_item.item_is_active = False  
    bid_item.save() 

    # Redirect back to main page 
    return HttpResponseRedirect(source_address)

# Show all categories               
def view_categories(request): 

    # Get categories. 
    categories = Category.objects.all()

    return render(request, "auctions/view_categories.html", {
            "categories": categories
        }) 

def view_listing_given_category(request, category):

    # Get all items related to that category (don't care about active status or not)
    category_row = Category.objects.get(category=category)
    items = Auction.objects.filter(item_category_id=category_row.id)
    print(category, items)

    return render(request, "auctions/view_specific_category.html", {
            "listings": items, 
            "category": category
        })

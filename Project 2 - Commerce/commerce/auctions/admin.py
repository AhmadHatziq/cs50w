from django.contrib import admin
from .models import User, Auction, Category, Bid, Comment 

# Create a new admin classes to see more details in the admin interface 
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email", "password", "last_login", "date_joined", "is_staff")
    
class AuctionAdmin(admin.ModelAdmin): 
    list_display =("id", "item_name", "item_owner", "item_starting_bid", "item_description", "item_image_url", 
        "item_category)
        
class CategoryAdmin(admin.ModelAdmin): 
    list_display = ("id", "category")
    
class BidAdmin(admin.ModelAdmin): 
    list_display = ("id", "bid_item", "bid_amount", "bid_bidder")
    
class CommentAdmin(admin.ModelAdmin): 
    list_display = ("id", "comment_string", "comment_user", "comment_listing")

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Auction, AuctionAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)
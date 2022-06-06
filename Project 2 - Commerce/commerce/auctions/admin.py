from django.contrib import admin
from .models import User, Auction, Category

# Create a new admin classes to see more details in the admin interface 
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email", "password", "last_login", "date_joined", "is_staff")
    
class AuctionAdmin(admin.ModelAdmin): 
    list_display =("id", "item_name", "item_owner", "item_bid_amount", "item_bid_count", "item_image_url", 
        "item_category")
        
class CategoryAdmin(admin.ModelAdmin): 
    list_display = ("id", "category")

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Auction, AuctionAdmin)
admin.site.register(Category, CategoryAdmin)
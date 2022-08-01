from django.contrib import admin
from .models import User, Geocache, DiscussionBoard

class UserAdmin(admin.ModelAdmin):      
    list_display = ("id", "username", "email", "password", "last_login", "date_joined", "is_staff")

class GeocacheAdmin(admin.ModelAdmin): 
    list_display = ("id", "latitude", "longitude", "isFound", "poster", "get_founders", "expiry_time", "timestamp", "get_users_following")

class DiscussionBoardAdmin(admin.ModelAdmin): 
    list_display = ("id", "geocache", "comment_poster", "comment_text", "comment_image", "timestamp")

# Register the models. 
admin.site.register(User, UserAdmin)
admin.site.register(Geocache, GeocacheAdmin)
admin.site.register(DiscussionBoard, DiscussionBoardAdmin)

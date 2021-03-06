from django.contrib import admin
from .models import User, Post, Like, FollowRelation

class UserAdmin(admin.ModelAdmin): 
    list_display = ("id", "username", "email", "password", "last_login", "date_joined", "is_staff")

class PostAdmin(admin.ModelAdmin):         
    list_display = ("id", "post_text_content", "post_user", "post_timestamp")

class LikeAdmin(admin.ModelAdmin): 
    list_display = ("id", "liked_post", "get_users_that_liked")

class FollowRelationAdmin(admin.ModelAdmin): 
    list_display = ("id", "follower", "get_users_being_followed")

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Like, LikeAdmin)
admin.site.register(FollowRelation, FollowRelationAdmin)

from django.contrib import admin
from .models import User 

class UserAdmin(admin.ModelAdmin): 
    list_display = ("id", "username", "email", "password", "last_login", "date_joined", "is_staff")

# Register your models here.
admin.site.register(User, UserAdmin)

from django.contrib import admin
from .models import Email, User 

# Create the admin classes to view the details in the admin interface ------------------------------------------------
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email", "password", "last_login", "date_joined")

class EmailAdmin(admin.ModelAdmin): 
    list_display = ("id", "user", "sender", "subject", "body", "timestamp", "read", "archived")

# Register your models here. -----------------------------------------------------------------------------------------
admin.site.register(User, UserAdmin)
admin.site.register(Email, EmailAdmin)


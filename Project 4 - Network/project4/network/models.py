from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    
    users_following = models.ManyToManyField("self", blank=True, related_name='following')
    users_follower = models.ManyToManyField("self", blank=True, related_name='follower')

    def __str__(self): 
        return f"{self.username}"

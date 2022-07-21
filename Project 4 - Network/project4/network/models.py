from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    def __str__(self): 
        return f"{self.username}"

class FollowRelation(models.Model): 
    follower = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'follower_user')
    users_following = models.ManyToManyField(User, blank = True, related_name = 'users_following')

    def __str__(self):   
        return f"{self.follower.username}"

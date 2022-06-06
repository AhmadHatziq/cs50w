from django.contrib.auth.models import AbstractUser
from django.db import models

'''
    Inherits from AbstractUser
'''
class User(AbstractUser):
    
    def __str__(self):
        return self.email

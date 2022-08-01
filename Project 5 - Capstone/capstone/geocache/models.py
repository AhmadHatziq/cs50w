from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Represents a single User. 
    """
    def __str__(self): 
        return f"{self.username}"
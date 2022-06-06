from django.contrib.auth.models import AbstractUser
from django.db import models

'''
    Inherits from AbstractUser
'''
class User(AbstractUser):
    
    def __str__(self):
        return f"{self.username}"

'''
    An auction listing can have similar categories. 
'''        
class Category(models.Model):
    category = models.CharField(max_length=64)
    
    def __str__(self): 
        return f"{self.category}"
    
    
class Auction(models.Model): 
    item_name = models.CharField(max_length=64)
    item_category = models.ForeignKey(Category, on_delete=models.PROTECT, db_column="category")
    item_owner = models.ForeignKey(User, on_delete=models.CASCADE)
    item_bid_amount = models.DecimalField(max_digits=9, decimal_places=2)
    item_bid_count = models.IntegerField(default=1) 
    item_image_url = models.URLField(max_length=256)
    
    def __str__(self): 
        return f"{self.item_name}"

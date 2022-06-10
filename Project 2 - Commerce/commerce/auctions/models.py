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
    item_image_url = models.URLField(max_length=256)
    item_starting_bid = models.DecimalField(max_digits=9, decimal_places=2)
    item_description = models.CharField(max_length=255)
    item_is_active = models.BooleanField(default=True)
    users_watching = models.ManyToManyField(User, blank=True, related_name='watching') # Call by (User obj).watching.all()
    
    def __str__(self): 
        return f"{self.item_name} by {self.item_owner} of category {self.item_category}"
        
class Bid(models.Model): 
    bid_amount = models.DecimalField(max_digits=9, decimal_places=2)
    bid_item = models.ForeignKey(Auction, on_delete=models.PROTECT)
    bid_bidder = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self): 
        return f"${self.bid_amount} for {self.bid_item.item_name} made by {self.bid_bidder}"
        
class Comment(models.Model): 
    comment_string = models.CharField(max_length=255)
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE) 
    comment_listing = models.ForeignKey(Auction, on_delete=models.CASCADE)
    
    def __str__(self): 
        return f"Comment '{self.comment_string}' was made by {self.comment_user} for item '{self.comment_listing}'"
        
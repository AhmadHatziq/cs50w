from django.contrib.auth.models import AbstractUser
from django.db import models
from geoposition.fields import GeopositionField


class User(AbstractUser):
    """
    Represents a single User. 
    """
    def __str__(self): 
        return f"{self.username}"

class Geocache(models.Model): 
    """
    Represents a geocache. Contains the user that created this, the geolocation, current status (found or opened). 
    Each geocache location has a limited time to be solved. 
    """
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    title = models.CharField(max_length=255)
    hint = models.CharField(max_length=255, blank=True)
    isFound = models.BooleanField(default=False)
    poster = models.ForeignKey(User, on_delete=models.CASCADE, related_name='poster')
    founder = models.ManyToManyField(User, blank=True, related_name='founder')
    users_following =  models.ManyToManyField(User, blank=True, related_name='users_following')
    timestamp = models.DateTimeField(auto_now_add=True)
    # position = GeopositionField()

    def __str__(self): 
        return f"Location is {self.latitude} lat, {self.longitude} lon. Title is {self.title}. Posted by {self.poster.username}"

    def get_users_following(self): 
        return "\n".join([u.username for u in self.users_following.all()])

    def get_founders(self): 
        return "\n".join([u.username for u in self.founder.all()])


class DiscussionBoard(models.Model): 
    """
    Represents the discussion board regarding a single geocache. Is made of comments (text and images) from people discussing. 
    First post is the hint from the poster regarding the location of the geocache. 
    """
    geocache = models.ForeignKey(Geocache, on_delete=models.CASCADE)
    comment_poster = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.CharField(max_length=255, blank=True)
    comment_image = models.ImageField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self): 
        return f"Comment made for geocache #{self.geocache.id} posted by {self.comment_poster.username} at {self.timestamp}. Comment: {self.comment_text}"

'''
class PointOfInterest(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=10)
    position = GeopositionField(blank=True)

    class Meta:
        verbose_name_plural = 'points of interest'
'''


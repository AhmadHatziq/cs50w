from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Represents a single User. 
    """
    def __str__(self): 
        return f"{self.username}"


class FollowRelation(models.Model): 
    """
    Represents the single relationship of a User following other User(s). 
    There will always be a single FollowRelation for each User. 
    When a User follows a new User, a FollowRelation is either created (for the first follow) or edited & appended. 
    If A is following B & C, there will be a single entry where: A -> (B, C)
        follower: A 
        users_following: B, C 
    """
    follower = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'follower_user')
    users_following = models.ManyToManyField(User, blank = True, related_name = 'users_following')

    def __str__(self):   
        return f"{self.follower.username}"

    def get_users_being_followed(self): 
        return "\n".join([u.username for u in self.users_following.all()])

class Post(models.Model): 
    """
    Represents a single textual post created by a user. 
    """
    post_text_content = models.CharField(max_length=255)
    post_user =  models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'comment_poster')
    post_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self): 
        return f"Post content: '{self.post_text_content}'. Posted by: {self.post_user.username}"

class Like(models.Model): 
    """
    Represents a Like of a Post by a group of user(s). Will be automatically created for each new Post. 
    """
    liked_post = models.ForeignKey(Post, on_delete = models.CASCADE) 
    liked_by_users = models.ManyToManyField(User, blank = True)

    def __str__(self): 
        return f"Like object for the post '{self.liked_post.post_text_content}' which is liked by: {self.get_users_that_liked()}"
    
    def get_users_that_liked(self): 
        return "\n".join([u.username for u in self.liked_by_users.all()])




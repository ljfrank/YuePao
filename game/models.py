from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    phone = models.CharField(max_length=20)
    follows = models.ManyToManyField("self", through='Follow', symmetrical=False)

class Tweet(models.Model):
    user = models.ForeignKey(User)
    content = models.CharField(max_length=200)
    time_posted = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    user = models.ForeignKey(User)
    tweet = models.ForeignKey(Tweet)
    time_posted = models.DateTimeField(auto_now_add=True)
    content = models.CharField(max_length=300)

class Follow(models.Model):
    followee = models.ForeignKey(UserProfile, related_name='asfollowee_set')
    follower = models.ForeignKey(UserProfile, related_name='asfollower_set')
    date_followed = models.DateTimeField(auto_now_add=True)
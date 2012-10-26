from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    phone = models.CharField(max_length=20)

class Tweet(models.Model):
    user = models.ForeignKey(User);
    content = models.CharField(max_length=140);
    time_posted = models.DateTimeField(auto_now_add=True);

class Comment(models.Model):
    user = models.ForeignKey(User);
    tweet = models.ForeignKey(Tweet);
    time_posted = models.DateTimeField(auto_now_add=True);
    content = models.CharField(max_length=300);

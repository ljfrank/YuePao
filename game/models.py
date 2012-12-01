from django.db import models
from django.contrib.auth.models import User
import datetime

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    phone = models.CharField(max_length=20)
    sex = models.CharField(max_length=1)
    born_date = models.DateField(default=datetime.date.today)
    follows = models.ManyToManyField("self", through='Follow', symmetrical=False)
    icon = models.ImageField(upload_to='headphotos',max_length=2097152)

class Tweet(models.Model):
    user = models.ForeignKey(UserProfile)
    content = models.CharField(max_length=200)
    time_posted = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now=True)
    retweet = models.ForeignKey('self', blank=True, null=True, on_delete=models.SET_NULL, related_name='original_tweet_set')
    original_tweet = models.ForeignKey('self', blank=True, null=True, on_delete=models.SET_NULL, related_name='retweet_set')
    retweet_count = models.IntegerField(default=0)
    deleted = models.BooleanField(default=False)

class Comment(models.Model):
    user = models.ForeignKey(UserProfile)
    tweet = models.ForeignKey(Tweet)
    time_commented = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now=True)
    content = models.CharField(max_length=200)

class Follow(models.Model):
    diaos = models.ForeignKey(UserProfile, related_name='as_diaos_set')
    goddess = models.ForeignKey(UserProfile, related_name='as_goddess_set')
    time_followed = models.DateTimeField(auto_now_add=True)

from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    phone = models.CharField(max_length=20)
    sex = models.CharField(max_length=1, choices=(('M','Male'),('F','Female')))
    born_date = models.DateField()
    follows = models.ManyToManyField("self", through='Follow', symmetrical=False)

class Tweet(models.Model):
    user = models.ForeignKey(User)
    content = models.CharField(max_length=200)
    time_posted = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now=True)
    retweet = models.ForeignKey('self', blank=True, null=True, on_delete=models.SET_NULL, related_name='original_tweet_set')
    original_tweet = models.ForeignKey('self', blank=True, null=True, on_delete=models.SET_NULL, related_name='retweet_set')
    retweet_count = models.IntegerField(default=0)
    deleted = models.BooleanField(default=False)

class Comment(models.Model):
    user = models.ForeignKey(User)
    tweet = models.ForeignKey(Tweet)
    time_commented = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now=True)
    content = models.CharField(max_length=200)

class Follow(models.Model):
    diaos = models.ForeignKey(UserProfile, related_name='as_diaos_set')
    goddess = models.ForeignKey(UserProfile, related_name='as_goddess_set')
    time_followed = models.DateTimeField(auto_now_add=True)

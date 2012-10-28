from game.forms import *
from game. models import *
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render_to_response

#Show all posts of a certain user.
@login_required
def posts(request, userID):
    return HttpResponse('!');

@login_required
def tweet(request):
    if request.method == 'POST':
        form = TweetForm(request.POST)
        if form.is_valid():
            tweet = Tweet(user=request.user, content=form.cleaned_data['tweet'])
            tweet.save()
    return redirect('/')

@login_required
def comment(request):
    if request.method == 'POST':
        return redirect('/')
    else:
        return redirect('/')

@login_required
def retweet(request):
    if request.method == 'POST':
        return redirect('/')
    else:
        return redirect('/')
   
@login_required
def watch(request):
    if request.method == 'POST':
        return redirect('/')
    else:
        return redirect('/')

@login_required
def star(request):
    if request.method == 'POST':
        return redirect('/')
    else:
        return redirect('/')

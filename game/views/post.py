from game.forms import *
from game.models import *
from game.statics import *
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render_to_response
from django.template import RequestContext

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
def retweet(request, tweetID):
    user = request.user
    try:
        retweet = Tweet.objects.get(id=tweetID)
        if retweet.deleted == True:
            return redirect('/')    #here we may need to redirect to an error page.
        if retweet.original_tweet and retweet.original_tweet.deleted == True:
            return redirect('/')    #here we may need to redirect to an error page.
    except Tweet.DoesNotExist :
        return redirect('/')    #here we may need to redirect to an error page.
    if request.method == 'POST':
        form = TweetForm(request.POST)
        if form.is_valid():
            original_tweet = retweet.original_tweet if retweet.original_tweet else retweet
            retweet.retweet_count += 1
            original_tweet.retweet_count += (1 if retweet.original_tweet else 0)
            retweet.save()
            original_tweet.save()
            tweet = Tweet(user=user, content=form.cleaned_data['tweet'], retweet=retweet, original_tweet=original_tweet)
            tweet.save()
        return redirect('/')
    else:
        original_content = '@' + retweet.user.username + ': ' + retweet.content if retweet.retweet else ''
        original_tweet = retweet.original_tweet if retweet.original_tweet else retweet
        return render_to_response(RETWEET_PATH, {'retweet':retweet, 'original_tweet':original_tweet, 'content':original_content}, context_instance=RequestContext(request))
   
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

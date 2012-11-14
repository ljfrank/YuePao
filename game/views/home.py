from game.forms import *
from game.helpers import *
from game.statics import *
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.http import require_GET

@require_GET
def home(request, form=None):
    if request.user.is_authenticated():
        if form is None:
            form = TweetForm()
        user = request.user;
        follows = Follow.objects.filter(diaos=user.userprofile)
        all_tweets = []
        for follow in follows:
            for tweet in follow.goddess.user.tweet_set.all():
                all_tweets.append(tweet)
        all_tweets.sort(key = lambda tweet:tweet.time_posted, reverse = True)
        return render_to_response(HOME_PATH, {'form':form, 'tweets':all_tweets}, context_instance=RequestContext(request))
    form = LogInForm()
    return render_to_response(WELCOME_PATH, {'form':form}, context_instance=RequestContext(request))

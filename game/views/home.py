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
        follows = list(Follow.objects.filter(diaos=user)) 
        follows.append(user.userprofile)
        tweets = Tweet.objects.filter(user__in=follows)
        return render_to_response(HOME_PATH, {'form':form, 'tweets':tweets}, context_instance=RequestContext(request))
    form = LogInForm()
    return render_to_response(WELCOME_PATH, {'form':form}, context_instance=RequestContext(request))

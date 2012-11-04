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
        return render_to_response(HOME_PATH, {'form':form}, context_instance=RequestContext(request))
    return render_to_response(WELCOME_PATH, context_instance=RequestContext(request))

from game.statics import *
from game.helpers import *
from django.shortcuts import render_to_response

def home(request):
    if request.user.is_authenticated():
        return render_to_response(HOME_PATH, {'user':request.user})
    return render_to_response(WELCOME_PATH)

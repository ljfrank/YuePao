from game.statics import *
from game.helpers import *
from django.shortcuts import render_to_response

def home(request):
    if user_logged_in(request):
        user = User.objects.get(username=request.session['username'])
        return render_to_response(HOME_PATH, {'user':user})
    else:
        return render_to_response(WELCOME_PATH, {})

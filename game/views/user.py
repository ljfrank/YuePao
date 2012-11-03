from game.statics import *
from game.helpers import *
from game.forms import *
from django.shortcuts import redirect, render_to_response
from django.template import RequestContext
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.views import logout as authlogout
from django.contrib.auth.decorators import login_required
from game.models import UserProfile

def login(request):
    if request.user.is_authenticated():
        return redirect('/')
    if request.method == 'GET':
        form = LogInForm()
        return render_to_response(LOGIN_PATH, {'form':form}, context_instance=RequestContext(request))
    if request.method == 'POST':
        form = LogInForm(request.POST)
        if form.is_valid():
            form.save(request)
            return redirect('/', {'user':user})
        else:
            return render_to_response(LOGIN_PATH, {'form':form}, context_instance=RequestContext(request))

def logout(request):
    return authlogout(request, next_page='/')

def signup(request):
    if request.user.is_authenticated():
        return redirect('/')
    if request.method == 'GET':
        form = SignUpForm()
        return render_to_response(SIGNUP_PATH, {'form':form}, context_instance=RequestContext(request))
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save(request)
            return redirect('/')
        return render_to_response(SIGNUP_PATH, {'form':form}, context_instance=RequestContext(request))

@login_required
def user(request, userID):
    try:
        showuser = User.objects.get(id=userID)
    except User.DoesNotExist:
        return users(request)
    user = request.user
    try:
        follow = Follow.objects.get(followee=showuser.userprofile, follower=user.userprofile)
    except Follow.DoesNotExist:
        follow = None
    except UserProfile.DoesNotExist:
        return users(request);
    tweets = showuser.tweet_set.all()
    return render_to_response(USER_PATH, {'showuser':showuser, 'tweets':tweets, 'user':request.user, 'follow':follow}, context_instance=RequestContext(request))

@login_required
def settings(request):
    if request.method == 'GET':
        form = ChangePWForm()
        return render_to_response(SETTING_PATH, {'form':form}, context_instance=RequestContext(request))
    if request.method == 'POST':
        form = ChangePWForm(request.POST)
        if form.is_valid():
            user.set_password(form.cleaned_data['password'])
            user.save()
        return render_to_response(SETTING_PATH, {'form':form}, context_instance=RequestContext(request))
    return redirect('/')

@login_required
def users(request):
    users = User.objects.all()
    return render_to_response(SHOWUSER_PATH, {'users':users, 'user':request.user}, context_instance=RequestContext(request))

@login_required
def follow(request, userID):
    user = request.user
    try:
        followee = User.objects.get(id=userID)
    except User.DoesNotExist:
        return redirect('/')
    try:
        follow = Follow.objects.get(followee=followee.userprofile, follower=user.userprofile)
        return redirect('/')
    except Follow.DoesNotExist:
        follow = Follow(followee=followee.userprofile, follower=user.userprofile)
        follow.save()
    return redirect('/')
    
@login_required
def unfollow(request, userID):
    user = request.user
    try:
        followee = User.objects.get(id=userID)
    except User.DoesNotExist:
        return redirect('/')
    try:
        follow = Follow.objects.get(followee=followee.userprofile, follower=user.userprofile)
        follow.delete()
        return redirect('/')
    except Follow.DoesNotExist:
        return redirect('/')

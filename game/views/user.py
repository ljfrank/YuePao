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

@login_required
def followed(request, userID):
    requested_user = User.objects.get(id = userID)
    user_profile = UserProfile.objects.get(user = requested_user)
    follows = Follow.objects.filter(diao_si = user_profile)
    user_profile_list = [follow.goddess for follow in follows]
    return users(request, user_profile_list)

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
        follow = Follow.objects.get(goddess=showuser.userprofile, diao_si=user.userprofile)
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
def users(request, user_list = None):
    if user_list == None:
        user_list = UserProfile.objects.all()
    return render_to_response(SHOWUSER_PATH, {'user_profiles':user_list, 'user':request.user}, context_instance=RequestContext(request))

@login_required
def follow(request, userID):
    user = request.user
    try:
        goddess = User.objects.get(id=userID)
    except User.DoesNotExist:
        return redirect('/')
    try:
        follow = Follow.objects.get(goddess=goddess.userprofile, diao_si=user.userprofile)
        return redirect('/')
    except Follow.DoesNotExist:
        follow = Follow(goddess=goddess.userprofile, diao_si=user.userprofile)
        follow.save()
    return redirect('/')
    
@login_required
def unfollow(request, userID):
    user = request.user
    try:
        ex_goddess = User.objects.get(id=userID)
    except User.DoesNotExist:
        return redirect('/')
    try:
        follow = Follow.objects.get(goddess=ex_goddess.userprofile, diao_si=user.userprofile)
        follow.delete()
        return redirect('/')
    except Follow.DoesNotExist:
        return redirect('/')

@login_required
def fans(request, userID):
    user = User.objects.get(id = userID)
    try:
        fans = Follow.objects.filter(goddess = user.userprofile)
        fansProfiles = []
        for fan in fans:
            fansProfiles.append(fan.diao_si)
    except Follow.DoesNotExist:
        fansProfiles = None
    return users(request, fansProfiles)

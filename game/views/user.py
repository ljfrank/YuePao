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
from django.http import HttpResponse

@login_required
def followed(request, userID):
    return users(request, getFollows(userID))

@login_required
def fans(request, userID):
    return users(request, getFans(userID))

def login(request):
    if request.user.is_authenticated():
        return redirect('/')
    if request.method == 'POST':
        form = LogInForm(request.POST)
        if form.is_valid():
            form.save(request)
            return redirect('/', {'user':user})
    return redirect('/')

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
        showuser = User.objects.get(id=userID).userprofile
        user = request.user.userprofile
    except User.DoesNotExist:
        return users(request)
    except UserProfile.DoesNotExist:
        return users(request)
    try:
        follow = Follow.objects.get(goddess=showuser, diaos=user)
    except Follow.DoesNotExist:
        follow = None
    tweets = showuser.tweet_set.all()
    return render_to_response(USER_PATH, {'showuser':showuser.user, 'tweets':tweets, 'user':request.user, 'follow':follow}, context_instance=RequestContext(request))

@login_required
def settings(request):
    if request.method == 'GET':
        form = SettingsForm()
        return render_to_response(SETTING_PATH, {'form':form}, context_instance=RequestContext(request))
    if request.method == 'POST':
        form = SettingsForm(request.POST)
        if form.is_valid():
            form.save(request)
            return redirect('/')
        return render_to_response(SETTING_PATH, {'form':form}, context_instance=RequestContext(request))
    return redirect('/')

@login_required
def users(request, user_list = None):
    if user_list == None:
        user_list = UserProfile.objects.all()
    return render_to_response(SHOWUSER_PATH, {'user_profiles':user_list, 'user':request.user}, context_instance=RequestContext(request))

@login_required
def follow(request, userID):
    try:
        user = request.user.userprofile
        goddess = User.objects.get(id=userID).userprofile
        if user==goddess:
            return redirect(request.META.get('HTTP_REFERER', '/'))
    except User.DoesNotExist, UserProfile.DoesNotExist:
        return redirect(request.META.get('HTTP_REFERER', '/'))
    try:
        follow = Follow.objects.get(goddess=goddess, diaos=user)
        return redirect(request.META.get('HTTP_REFERER', '/'))
    except Follow.DoesNotExist:
        follow = Follow(goddess=goddess, diaos=user)
        follow.save()
    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def unfollow(request, userID):
    try:
        user = request.user.userprofile
        goddess = User.objects.get(id=userID).userprofile
    except User.DoesNotExist, UserProfile.DoesNotExist:
        return redirect(request.META.get('HTTP_REFERER', '/'))
    try:
        follow = Follow.objects.get(goddess=goddess, diaos=user)
        follow.delete()
        return redirect(request.META.get('HTTP_REFERER', '/'))
    except Follow.DoesNotExist:
        return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def uploadIcon(request):
    user = request.user
    if request.method == 'POST':
        form = UploadIconForm(request.POST, request.FILES)
        if form.is_valid():
            profile = UserProfile.objects.get(user=user)
            profile.icon = request.FILES['icon']
            profile.save()
            return redirect('/');       #Upload avatar successfully.
    else:
        form = UploadIconForm()
    return render_to_response('user/_upload_head_photo.html', {'form': form, 'user': request.user}, context_instance=RequestContext(request))

def showIcon(request, userID):
    try:
        user = User.objects.get(id = userID)
        profile = UserProfile.objects.get(user=user)
        if (profile.icon):
            icon = profile.icon
            response = HttpResponse(icon, content_type='image/jpeg')
            return response
    except User.DoesNotExist:
        return redirect('/')    #here we may need to redirect to an error page.
    except UserProfile.DoesNotExist:
        return redirect('/')    #here we may need to redirect to an error page.
    return redirect('http://tp4.sinaimg.cn/2668684791/50/5626936701/1')     #redirect to the default avatar


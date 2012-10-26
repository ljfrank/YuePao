from game.statics import *
from game.helpers import *
from django import forms
from django.shortcuts import redirect, render_to_response
from django.template import RequestContext
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.views import logout as authlogout, login as authlogin
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
            user = authenticate(username = form.cleaned_data['username'], password = form.cleaned_data['password'])
            if user == None:
                return render_to_response(LOGIN_PATH, {'form':form, 'msgs':['not valid user']}, context_instance=RequestContext(request))
            authlogin(request, user)
            return redirect('/', {'user':user})
        else:
            return render_to_response(LOGIN_PATH, {'form':form}, context_instance=RequestContext(request))

class LogInForm(forms.Form):
    username = forms.CharField(label='username', required=True, max_length=20)
    password = forms.CharField(label='password', widget=forms.PasswordInput, required=True, max_length=20)

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
            try:
                user = User.objects.get(username=request.POST['username'])
            except User.DoesNotExist:
                user = User.objects.create_user(form.cleaned_data['username'], None, form.cleaned_data['password']);
                user_profile = UserProfile(user=user)
                user.save()
                user_profile.save()
                authlogin(request, user)
                return redirect('/')
        return render_to_response(SIGNUP_PATH, {'form':form}, context_instance=RequestContext(request))

class SignUpForm(forms.Form):
    username = forms.CharField(label='username', required=True, max_length=20)
    password = forms.CharField(label='password', widget=forms.PasswordInput, required=True, max_length=20)

@login_required
def user(request, userID):
    user = request.user
    if int(user.id) == int(userID):
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
    else:
        showuser = User.objects.get(id=userID)
        tweet = showuser.tweet_set.get(user=showuser);
        return render_to_response(USER_PATH, {'showuser':showuser, 'tweet':tweet})

class ChangePWForm(forms.Form):
    password = forms.CharField(label='New Password', widget=forms.PasswordInput, required=True, max_length=20)

@login_required
def users(request):
    users = User.objects.all()
    return render_to_response(SHOWUSER_PATH, {'users':users, 'user':request.user})

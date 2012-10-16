from game.statics import *
from game.helpers import *
from django import forms
from django.shortcuts import redirect, render_to_response
from django.template import RequestContext

def login(request):
    if user_logged_in(request):
        return redirect('/')
    if request.method == 'GET':
        form = LogInForm()
        return render_to_response(LOGIN_PATH, {'form':form, 'user':None}, context_instance=RequestContext(request))
    if request.method == 'POST':
        form = LogInForm(request.POST)
        if form.is_valid():
            user = validate_user(form.cleaned_data['username'], form.cleaned_data['password'])
            if user == None:
                return render_to_response(LOGIN_PATH, {'form':form, 'user':None}, context_instance=RequestContext(request))
            request.session['username'] = user.name
            return redirect('/', {'user':user})
        else:
            return render_to_response(LOGIN_PATH, {'form':form, 'user':None}, context_instance=RequestContext(request))

class LogInForm(forms.Form):
    username = forms.CharField(label='Username', required=True, max_length=20)
    password = forms.CharField(label='Password', widget=forms.PasswordInput, required=True, max_length=20)

def logout(request):
    if user_logged_in(request):
        del request.session['username']
    return render_to_response(WELCOME_PATH, {'user':None})

def signup(request):
    if user_logged_in(request):
        return redirect('/')
    if request.method == 'GET':
        form = SignUpForm()
        return render_to_response(SIGNUP_PATH, {'form':form, 'user':None}, context_instance=RequestContext(request))
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            try:
                user = User.objects.get(name=request.POST['username'])
            except User.DoesNotExist:
                user = User(name=form.cleaned_data['username'], password=form.cleaned_data['password'])
                user.save()
                request.session['username']=form.cleaned_data['username']
                return redirect('/user/'+str(user.id))
        return render_to_response(SIGNUP_PATH, {'form':form, 'user':None}, context_instance=RequestContext(request))

class SignUpForm(forms.Form):
    username = forms.CharField(label='Username', required=True, max_length=20)
    password = forms.CharField(label='Password', widget=forms.PasswordInput, required=True, max_length=20)

def user(request, userID):
    if not user_logged_in(request):
        return redirect('/')
    user = User.objects.get(name=request.session['username'])
    if int(user.id) == int(userID):
        if request.method == 'GET':
            form = ChangePWForm()
            return render_to_response(SETTING_PATH, {'form':form, 'user':user}, context_instance=RequestContext(request))
        if request.method == 'POST':
            form = ChangePWForm(request.POST)
            if form.is_valid():
                user.password = form.cleaned_data['password']
                user.save()
            return render_to_response(SETTING_PATH, {'form':form, 'user':user}, context_instance=RequestContext(request))
        return redirect('/')
    else:
        showuser = User.objects.get(id=userID)
        return render_to_response(USER_PATH, {'user':user, 'showuser':showuser})

class ChangePWForm(forms.Form):
    password = forms.CharField(label='New Password', widget=forms.PasswordInput, required=True, max_length=20)

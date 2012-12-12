from django import forms
from django.core import validators
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from game.models import *

class TweetForm(forms.Form):
    tweet = forms.CharField(max_length=200, required=True, widget=forms.Textarea(attrs={'rows':'3', 'cols':'67'}))

class SignUpForm(forms.Form):
    username = forms.CharField(label='username', required=True, min_length=1, max_length=20)
    password = forms.CharField(label='password', widget=forms.PasswordInput, required=True, min_length=6, max_length=20)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        try :
            User.objects.get(username=username)
        except User.DoesNotExist :
            return username
        raise validators.ValidationError('Username already existed. Plz modify.')

    def save(self, request):
        user = User.objects.create_user(self.cleaned_data['username'], None, self.cleaned_data['password']);
        user_profile = UserProfile(user=user)
        user.userprofile = user_profile
        user.save()
        user_profile.save()
        #add default gallery for new user
        gallery_icon = Gallery(name='Icons', description='', user=user_profile, private=True, able_to_delete=False)
        gallery_tweet_photo = Gallery(name='Photos in Tweets', description='', user=user_profile, private=True, able_to_delete=False)
        gallery_icon.save()
        gallery_tweet_photo.save()
        user = authenticate(username=self.cleaned_data['username'], password=self.cleaned_data['password'])
        login(request, user)
        return user

class SettingsForm(forms.Form):
    oldpassword = forms.CharField(label='Old password', widget=forms.PasswordInput, required=True, min_length=6, max_length=20)
    newpassword1 = forms.CharField(label='New password', widget=forms.PasswordInput, required=True, min_length=6, max_length=20)
    newpassword2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput, required=True, min_length=6, max_length=20)
    from django.forms.extras.widgets import SelectDateWidget
    borndate = forms.DateField(label='Born Date', widget=SelectDateWidget(years=range(1930,2012)))
    sex = forms.ChoiceField(label='Sex', widget=forms.Select, required=True, choices=(('M','Male'),('F','Female')))
    phone = forms.CharField(label='Phone', widget=forms.TextInput)

    def save(self, request):
        user = request.user
        user.password = self.cleaned_data.get('newpassword1')
        user.save()
        profile = UserProfile.objects.get(user=user)
        profile.sex = self.cleaned_data.get('xex')
        profile.born_date = self.cleaned_data.get('borndate')
        profile.phone = self.cleaned_data.get('phone')
        profile.save()
        return user

class UploadPhotoForm(forms.Form):
    photo = forms.ImageField(required=True, max_length=2097152)

class ClipPhotoForm(forms.Form):
    x = forms.IntegerField(required=True, min_value=0)
    y = forms.IntegerField(required=True, min_value=0)
    width = forms.IntegerField(required=True, min_value=0)
    height = forms.IntegerField(required=True, min_value=0)
    photo_name = forms.CharField(required=True, max_length=50)
    photo_width = forms.IntegerField(required=True, min_value=0)
    photo_height = forms.IntegerField(required=True, min_value=0)

class LogInForm(forms.Form):
    username = forms.CharField(label='username', required=True, max_length=20)
    password = forms.CharField(label='password', widget=forms.PasswordInput, required=True, max_length=20)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        try:
            User.objects.get(username=username)
            return username
        except User.DoesNotExist:
            raise validators.ValidationError('Not valid username. You may want to signup first.')

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if authenticate(username=username, password=password) is None : raise validators.ValidationError('Password is not correct. Maybe check Caps Lock?')
        return self.cleaned_data

    def save(self, request):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        return user

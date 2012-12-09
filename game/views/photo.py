from game.statics import *
from game.helpers import *
from game.forms import *
from mysite.settings import *
from django.shortcuts import redirect, render_to_response
from django.template import RequestContext
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.views import logout as authlogout
from django.contrib.auth.decorators import login_required
from game.models import UserProfile
from django.http import HttpResponse
from django.utils import simplejson
from django.views.decorators.csrf import csrf_exempt
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image
from cStringIO import StringIO
import time
import os

@login_required
def iconPreview(request, photoName = None):
    response_data = {}
    user = UserProfile.objects.get(user=request.user)
    if request.method == 'GET':
        if photoName == None or photoName == '':
            response_data['error'] = 'Invalid Access'
            response = HttpResponse(simplejson.dumps(response_data))
        else:
            try:
                photo = Photograph.objects.get(user=user, name=photoName)
                img = Image.open(photo.photo.path)
                return render_to_response('user/_clip_icon.html', {'user':request.user, 'photoName':photoName, 'width':img.size[0], 'height':img.size[1]}, context_instance=RequestContext(request))
            except Photograph.DoesNotExist:
                response_data['error'] = 'This photo does not exist!'
                response = HttpResponse(simplejson.dumps(response_data))
    else:
        if photoName == None or photoName == '':
            form = UploadPhotoForm(request.POST, request.FILES)
            if form.is_valid():
                img = request.FILES['photo']
                name = request.user.username + '-' + time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time())) + img.name[img.name.rfind('.'):]
                img.name = name
                photo = Photograph(name=name, photo=img, user=user)
                photo.save()
                photo.name = photo.photo.name[photo.photo.name.rfind('/')+1:]
                photo.save()
                img = Image.open(photo.photo.path)
                width = img.size[0]
                height = img.size[1]
                if width > 600 or height > 600:
                    scale = 600.0 / max(width, height)
                    img = img.resize((int(width * scale),int(height * scale)))
                    img.save(photo.photo.path)
                response_data['name'] = name
                response = HttpResponse(simplejson.dumps(response_data))
            else:
                response_data['error'] = 'Error occured! Please check your file.'
                response = HttpResponse(simplejson.dumps(response_data))
        else:
            response_data['error'] = 'Invalid Access'
            response = HttpResponse(simplejson.dumps(response_data))
    return response

@login_required
@csrf_exempt
def uploadIcon(request):
    response_data = {}
    if request.method == 'POST':
        form = ClipPhotoForm(request.POST)
        if form.is_valid():
            try:
                x = form.cleaned_data['x']
                y = form.cleaned_data['y']
                width = form.cleaned_data['width']
                height = form.cleaned_data['height']
                photo_name = form.cleaned_data['photo_name']
                name = request.user.username + '-' + time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time())) + photo_name[photo_name.rfind('.'):]
                user = UserProfile.objects.get(user=request.user)
                path = Photograph.objects.get(user=user, name=photo_name).photo.path
                img = Image.open(path)
                img = img.crop((x, y, x+width, y+height))
                path = os.path.join(MEDIA_ROOT, 'icons/')
                if not os.path.exists(path):
                    os.makedirs(path)
                path = path + name
                print path
                img.save(path)
                print 3
                user.icon = path
                user.save()
                print 4
                response_data['success'] = 'success'
            except Photograph.DoesNotExist:
                response_data['error'] = 'Invalid post data!'
        else:
            response_data['error'] = 'Invalid post data!'
            #print form.errors
        response = HttpResponse(simplejson.dumps(response_data))
    else:
        form = UploadPhotoForm()
        response = render_to_response('user/_upload_head_photo.html', {'form': form, 'user': request.user}, context_instance=RequestContext(request))
    return response

def showIcon(request, userID):
    try:
        user = User.objects.get(id = userID).userprofile 
        if (user.icon):
            icon_path = user.icon
            print icon_path
            img = Image.open(icon_path)
            buf = StringIO()
            img.save(buf, "jpeg")
            return HttpResponse(buf.getvalue(), content_type='image/jpeg')
    except User.DoesNotExist:
        return redirect('/')    #here we may need to redirect to an error page.
    return redirect('http://tp4.sinaimg.cn/2668684791/50/5626936701/1')     #redirect to the default avatar

def showPhoto(request, userID, photoName):
    try:
        user = User.objects.get(id = userID).userprofile
        photo = Photograph.objects.get(user=user, name=photoName).photo
        response = HttpResponse(photo, content_type='image/jpeg')
    except User.DoesNotExist, UserProfile.DoesNotExist:
        response = HttpResponse('User does not exist!')
    except Photograph.DoesNotExist:
        response = HttpResponse('Photo does not exist!')
    return response


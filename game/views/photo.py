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
from django.views.decorators.http import require_http_methods
from PIL import Image
from cStringIO import StringIO
import time
import os

@login_required
def uploadPhoto(request, isIcon = False):
    response_data = {}
    if request.method == 'POST':
        form = UploadPhotoForm(request.POST, request.FILES)
        if form.is_valid():
            img = request.FILES['photo']
            path = os.path.join(MEDIA_ROOT, time.strftime('photos/%Y/%m/%d',time.localtime(time.time())))
            name = request.user.username + '-' + time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time())) + img.name[img.name.rfind('.'):]
            img.name = name
            user = UserProfile.objects.get(user=request.user)
            if isIcon:
                photo = Photograph(name=name, photo=img, user=user, gallery=Gallery.objects.get(name='Icons', user=user))
            else:
                photo = Photograph(name=name, photo=img, user=user, gallery=Gallery.objects.get(name='Photos in Tweets', user=user))
            photo.save()
            photo.name = photo.photo.name[photo.photo.name.rfind('/')+1:]
            photo.save()
            #create a thumbnail image
            img = Image.open(photo.photo.path)
            width = img.size[0]
            height = img.size[1]
            path = os.path.join(path, 'thumb/')
            if not os.path.exists(path):
                os.makedirs(path)
            path = path + name
            if height > 80:
                scale = 80.0 / height
                img = img.resize((int(width * scale),int(height * scale)))
                width = img.size[0]
                height = img.size[1]
                if width > 160:
                    img = img.crop((int(width/2)-80, 0, int(width/2)+80, height))
                img.save(path)
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
def deletePhoto(request):
    response_data = {}
    if request.method == 'POST':
        try:
            photoName = request.POST['photo_name']
            photo = Photograph.objects.get(name=photoName, user=request.user.userprofile)
            photo.delete()
            response_data['success'] = 'successful'
            response = HttpResponse(simplejson.dumps(response_data))
        except Photograph.DoesNotExist:
            response_data['error'] = 'Photo does not exist!'
            response = HttpResponse(simplejson.dumps(response_data))
    else:
        response_data['error'] = 'Invalid Access'
        response = HttpResponse(simplejson.dumps(response_data))
    return response

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
                width = img.size[0]
                height = img.size[1]
                if width > 600 or height > 600:
                    scale = 600.0 / max(width, height)
                    width = int(width * scale)
                    height = int(height * scale)
                return render_to_response('user/_clip_icon.html', {'user':request.user, 'photoName':photoName, 'width':width, 'height':height}, context_instance=RequestContext(request))
            except Photograph.DoesNotExist:
                response_data['error'] = 'This photo does not exist!'
                response = HttpResponse(simplejson.dumps(response_data))
    else:
        if photoName == None or photoName == '':
            return uploadPhoto(request, True)
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
                photo_width = form.cleaned_data['photo_width']
                photo_height = form.cleaned_data['photo_height']
                name = request.user.username + '-' + time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time())) + photo_name[photo_name.rfind('.'):]
                user = UserProfile.objects.get(user=request.user)
                path = Photograph.objects.get(user=user, name=photo_name).photo.path
                img = Image.open(path)
                img = img.resize((photo_width, photo_height))
                img = img.crop((x, y, x+width, y+height))
                path = os.path.join(MEDIA_ROOT, 'icons/')
                if not os.path.exists(path):
                    os.makedirs(path)
                path = path + name
                img.save(path)
                user.icon = path
                user.save()
                response_data['success'] = 'success'
            except Photograph.DoesNotExist:
                response_data['error'] = 'Invalid post data!'
        else:
            response_data['error'] = 'Invalid post data!'
            #print form.errors
        response = HttpResponse(simplejson.dumps(response_data))
    else:
        response = render_to_response('user/_upload_head_photo.html', {'user': request.user}, context_instance=RequestContext(request))
    return response

@require_http_methods(["GET"])
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

@require_http_methods(["GET"])
def showPhoto(request, userID, photoName):
    try:
        user = User.objects.get(id = userID).userprofile
        photo = Photograph.objects.get(user=user, name=photoName).photo
        #Show thumbnail image
        if request.GET.has_key('type') and request.GET['type'] == 'thumb':
            path = photo.path
            path = path[ : path.rfind('\\')] + '\\thumb' + path[path.rfind('\\') : ]
            img = Image.open(path)
            buf = StringIO()
            img.save(buf, "jpeg")
            return HttpResponse(buf.getvalue(), content_type='image/jpeg')
        else:
            return HttpResponse(photo, content_type='image/jpeg')
    except User.DoesNotExist, UserProfile.DoesNotExist:
        return HttpResponse('User does not exist!')
    except Photograph.DoesNotExist:
        return HttpResponse('Photo does not exist!')


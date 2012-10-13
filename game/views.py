from django.http import HttpResponse
from django.template import Context, loader, RequestContext
from django.shortcuts import redirect, render_to_response
from django.core.context_processors import csrf
from game.models import User

def home(request):
    if 'username' in request.session:
        t = loader.get_template('game/templates/home.html')
        c = Context({'user':request.session.get('username')})
        return HttpResponse(t.render(c))
    else:
        t = loader.get_template('game/templates/welcome.html')
        c = Context({})
        return HttpResponse(t.render(c))

def logout(request):
    request.session.pop('username')
    return redirect('home')

def login(request):
    if 'username' in request.session:
        return redirect('home')
    if request.method == 'POST':
        try:
            user = User.objects.get(name=request.POST['username'])
            if user.password != request.POST['password']:
                return HttpResponse('password not correct.')
            request.session['username']=request.POST['username']
            return redirect('/user/'+str(user.id)+'/')
        except User.DoesNotExist:
            return HttpResponse('not valid username!')
    if request.method == 'GET':
        t = loader.get_template('game/templates/login.html')
        c = RequestContext(request)
        return HttpResponse(t.render(c))

def signup(request):
    if 'username' in request.session:
        return redirect('home')
    if request.method == 'GET':
        t = loader.get_template('game/templates/signup.html')
        c = RequestContext(request)
        return HttpResponse(t.render(c))
    if request.method == 'POST':
        try:
            user = User.objects.get(name=request.POST['username'])
        except User.DoesNotExist:
            user = User(name=request.POST['username'], password=request.POST['password'])
            user.save()
            request.session['username']=request.POST['username']
            return redirect('user/'+user.id)

def user(request, userID):
    if 'username' not in request.session:
        return redirect('home')
    if request.method =='GET':
        user = User.objects.get(id=userID)
        return render_to_response('game/templates/user.html', {'user': user})

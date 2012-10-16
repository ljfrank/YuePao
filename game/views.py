from django.http import HttpResponse
from django.template import Context, loader, RequestContext
from django.shortcuts import redirect, render_to_response
from django.core.context_processors import csrf
from game.models import User

welcome_path = 'home/welcome.html'
user_path = 'user/user.html'
login_path = 'user/login.html'
signup_path = 'user/signup.html'

def user_logged_in(request):
    return 'username' in request.session

def nav_link(request):
    ret={}
    ret['Home']='/'
    if user_logged_in(request):
        user = User.objects.get(name=request.session['username'])
        ret['Log Out']='/logout/'
        ret['User']='/user/'+str(user.id)+'/'
    else:
        ret['Log In']='/login/'
    return ret

def home(request):
    t = loader.get_template(welcome_path)
    c = Context({'nav':nav_link(request)})
    return HttpResponse(t.render(c))

def logout(request):
    request.session.pop('username')
    return redirect('home')

def login(request):
    if user_logged_in(request):
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
        t = loader.get_template(login_path)
        c = RequestContext(request, {''})
        return HttpResponse(t.render(c))

def signup(request):
    if 'username' in request.session:
        return redirect('home')
    if request.method == 'GET':
        t = loader.get_template('signup.html')
        c = RequestContext(request)
        return HttpResponse(t.render(c))
    if request.method == 'POST':
        try:
            user = User.objects.get(name=request.POST['username'])
        except User.DoesNotExist:
            user = User(name=request.POST['username'], password=request.POST['password'])
            user.save()
            request.session['username']=request.POST['username']
            return redirect('user/'+str(user.id))

def user(request, userID):
    if 'username' not in request.session:
        return redirect('home')
    if request.method =='GET':
        user = User.objects.get(id=userID)
        return render_to_response('user.html', {'user': user})

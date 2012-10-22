from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

#Show all posts of a certain user.
@login_required
def posts(request, userID):
    return HttpResponse('!');

@login_required
def showJB(request):
    if request.method == 'POST':
        return redirect('/')
    else:
        return redirect('/')

@login_required
def makeLove(request):
    if request.method == 'POST':
        return redirect('/')
    else:
        return redirect('/')

@login_required
def showPussy(request):
    if request.method == 'POST':
        return redirect('/')
    else:
        return redirect('/')
   
@login_required
def buyPorn(request):
    if request.method == 'POST':
        return redirect('/')
    else:
        return redirect('/')

@login_required
def makePornMovie(request):
    if request.method == 'POST':
        return redirect('/')
    else:
        return redirect('/')

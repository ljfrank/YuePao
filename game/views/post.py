from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

#Show all posts of a certain user.
@login_required
def posts(request, userID):
    return HttpResponse('!');

@login_required
def tweet(request):
    if request.method == 'POST':
        return redirect('/')
    else:
        return redirect('/')

@login_required
def comment(request):
    if request.method == 'POST':
        return redirect('/')
    else:
        return redirect('/')

@login_required
def retweet(request):
    if request.method == 'POST':
        return redirect('/')
    else:
        return redirect('/')
   
@login_required
def watch(request):
    if request.method == 'POST':
        return redirect('/')
    else:
        return redirect('/')

@login_required
def star(request):
    if request.method == 'POST':
        return redirect('/')
    else:
        return redirect('/')

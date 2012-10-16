from game.models import UserProfile
from django.contrib.auth.models import User

def user_logged_in(request):
    return 'username' in request.session

def validate_user(username, password):
    try:
        user = User.objects.get(name=username)
        if user.password != password:
            return None
        return user
    except User.DoesNotExist:
        return None

from models import *

def getFollows(userID):
    user = User.objects.get(id=userID).userprofile
    try:
        follows = list(Follow.objects.filter(diaos=user))
        goddesses = [follow.goddess for follow in follows]
    except Follow.DoesNotExist:
        goddesses = []
    return goddesses

def getFans(userID):
    user = User.objects.get(id=userID).userprofile
    try:
        follows = list(Follow.objects.filter(goddess=user))
        diaos = [follow.diaos for follow in follows]
    except Follow.DoesNotExist:
        diaos = []
    return diaos

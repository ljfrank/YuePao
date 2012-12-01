def getFollows(userID):
    user = User.objects.get(id=userID).userprofile
    try:
        follows = list(Follow.objects.filter(diaos=user))
    except Follow.DoesNotExist:
        follows = []
    return follows

def getFans(userID):
    user = User.objects.get(id=userID).userprofile
    try:
        fans = list(Follow.objects.filter(goddess=user))
    except Follow.DoesNotExist:
        fans = []
    return fans

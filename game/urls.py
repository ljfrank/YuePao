from django.conf.urls import patterns, include, url

urlpatterns = patterns('game.views.home',
    url(r'^/?$', 'home'),
)

urlpatterns += patterns('game.views.user',
    url(r'^login/?$', 'login'),
    url(r'^logout/?$', 'logout'),
    url(r'^signup/?$', 'signup'),
    url(r'^user/(?P<userID>\d+)/?$', 'user'),
    url(r'^user/?$', 'users'),
)

urlpatterns += patterns('game.views.post',
    url(r'^user/(?P<userID>\d+)/posts/?$', 'posts'),
    url(r'^showJB/?$', 'tweet'),
    url(r'^makeLove/?$', 'comment'),
    url(r'^showPussy/?$', 'retweet'),
    url(r'^buyPorn/?$', 'watch'),  
    url(r'^makePornMovie/?$', 'star'),
)

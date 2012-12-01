from django.conf.urls import patterns, include, url

urlpatterns = patterns('game.views.home',
    url(r'^/?$', 'home'),
)

urlpatterns += patterns('game.views.user',
    url(r'^login/?$', 'login'),
    url(r'^logout/?$', 'logout'),
    url(r'^signup/?$', 'signup'),
    url(r'^settings/?', 'settings'),
    url(r'^user/?$', 'users'),
    url(r'^user/(?P<userID>\d+)/?$', 'user'),
    url(r'^user/(?P<userID>\d+)/followed/?$', 'followed'),
    url(r'^user/(?P<userID>\d+)/fans/?$', 'fans'),
    url(r'^follow/(?P<userID>\d+)/?$', 'follow'),
    url(r'^unfollow/(?P<userID>\d+)/?$', 'unfollow'),
    url(r'^user/upload/icon/?$', 'uploadIcon'),
    url(r'^user/(?P<userID>\d+)/icon/?$', 'showIcon'),
)

urlpatterns += patterns('game.views.post',
    url(r'^user/(?P<userID>\d+)/posts/?$', 'posts'),
    url(r'^showJB/?$', 'tweet'),
    url(r'^makeLove/?$', 'comment'),
    url(r'^tweet/(?P<tweetID>\d+)/retweet/?$', 'retweet'),
    url(r'^buyPorn/?$', 'watch'),
    url(r'^makePornMovie/?$', 'star'),
)

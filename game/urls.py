from django.conf.urls import patterns, include, url

urlpatterns = patterns('game.views.home',
    url(r'^/?$', 'home'),
)

urlpatterns += patterns('game.views.user',
    url(r'^login/?$', 'login'),
    url(r'^logout/?$', 'logout'),
    url(r'^signup/?$', 'signup'),
    url(r'^settings/?', 'settings'),
    url(r'^notifications/?', 'notifications'),
    url(r'^user/?$', 'users'),
    url(r'^user/(?P<userID>\d+)/?$', 'user'),
    url(r'^user/(?P<userID>\d+)/followed/?$', 'followed'),
    url(r'^user/(?P<userID>\d+)/fans/?$', 'fans'),
    url(r'^follow/(?P<userID>\d+)/?$', 'follow'),
    url(r'^unfollow/(?P<userID>\d+)/?$', 'unfollow'),
)

urlpatterns += patterns('game.views.post',
    url(r'^user/(?P<userID>\d+)/posts/?$', 'posts'),
    url(r'^showJB/?$', 'tweet'),
    url(r'^makeLove/?$', 'comment'),
    url(r'^tweet/(?P<tweetID>\d+)/retweet/?$', 'retweet'),
    url(r'^buyPorn/?$', 'watch'),
    url(r'^makePornMovie/?$', 'star'),
)

urlpatterns += patterns('game.views.photo',
    url(r'^upload/icon/preview/(?P<photoName>[\w.-]+)/?$', 'iconPreview'),
    url(r'^upload/icon/preview/?$', 'iconPreview'),
    url(r'^upload/icon/?$', 'uploadIcon'),
    url(r'^user/(?P<userID>\d+)/icon/?$', 'showIcon'),
    url(r'^user/(?P<userID>\d+)/(?P<photoName>[\w.-]+)/?$', 'showPhoto'),
    url(r'^upload/photo/?$', 'uploadPhoto'),
    url(r'^delete/photo/?$', 'deletePhoto'),
)

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

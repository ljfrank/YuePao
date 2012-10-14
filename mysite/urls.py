from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^logout/$', 'game.views.logout', name='logout'),
    url(r'^login/$', 'game.views.login', name='login'),
    url(r'^signup/$', 'game.views.signup', name='signup'),
    url(r'^user/(?P<userID>\d+)/$', 'game.views.user'),
    url(r'^$', 'game.views.home', name='home'),
    # url(r'^mysite/', include('mysite.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

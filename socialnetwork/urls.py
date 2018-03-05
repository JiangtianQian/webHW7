"""webapps URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import *
from django.contrib import admin
from django.contrib.auth import views as auth_views
from socialnetwork import views

urlpatterns = [
    url(r'^login$', auth_views.login,{'template_name':'socialnetwork/login.html'},name='login'),

    # ?????
    url(r'^accounts/login/$', auth_views.login,{'template_name':'socialnetwork/login.html'}),
    url(r'^accounts/login$', auth_views.login,{'template_name':'socialnetwork/login.html'}),
    # ?????
    url(r'^register$', views.register,name='register'),
    url(r'^register/$', views.register,name='register'),
    # url(r'^accounts/register/$', views.register, name='register'),
    url(r'^home$', views.home, name='home'),
    url(r'^home/$', views.home, name='home'),
    url(r'^accounts/profile/$', views.home),
    # url(r'^accounts/login', auth_views.login,{'template_name':'grumblr/SignIn.html'},name='login'),
    url(r'^logout$', auth_views.logout_then_login,name = 'logout'),
    url(r'^logout/$', auth_views.logout_then_login,name = 'logout'),
    url(r'^myProfile$', views.myProfile, name = 'myProfile'),
    url(r'^myProfile/$', views.myProfile, name = 'myProfile'),
    url(r'^updateProfile$', views.updateProfile, name = 'updateProfile'),
    url(r'^updateProfile/$', views.updateProfile, name = 'updateProfile'),
    url(r'^otherProfile/(?P<userid>[a-zA-Z0-9_@\+\-]+)$', views.otherProfile, name = 'otherProfile'),
    url(r'^otherProfile/(?P<userid>[a-zA-Z0-9_@\+\-]+)$', views.otherProfile, name = 'otherProfile'),
    # url(r'^photo/(?P<id>\d+)$', views.getphoto, name = 'photo'),
    url(r'^photo/(?P<userid>\d+)$', views.get_photo, name='photo'),
    url(r'^confirm/(?P<username>[a-zA-Z0-9_@\+\-]+)/(?P<token>[a-z0-9\-]+)$', views.confirm, name = 'confirm'),
    url(r'^confirm/(.*)', views.confirm, name = 'confirm'),
    url(r'^follow/$', views.followStream, name = 'followStream'),
    url(r'^follow/(.*)$', views.follow, name = 'follow'),

    url(r'^unFollow/(.*)$', views.unFollow, name = 'unFollow'),

    # url(r'^register/login/$', auth_views.login,{'template_name':'grumblr/SignIn.html'},name='login'),
    # url(r'^accounts/logout$', auth_views.logout_then_login),
    #  url(r'^', auth_views.login,{'template_name':'grumblr/SignIn.html'},name='login'),
    url(r'^get-items/?$', views.get_items),
    url(r'^get-items/(?P<time>.+)$', views.get_items),
    url(r'^get-changes/?$', views.get_changes),
    url(r'^get-changes/(?P<time>.+)$', views.get_changes),
    # url(r'^get-changesInprofile/(?P<time>.+)/(?P<username>[a-zA-Z0-9_@\+\-]+)/$', views.get_changeInProfile),
    
    url(r'^get-changesComment/?$', views.get_commentchanges),
    url(r'^get-changesComment/(?P<time>.+)/(?P<item_id>\d+)/$', views.get_commentchanges),
    url(r'^get-allComment/?$', views.get_commentall),
    url(r'^get-allComment/(?P<item_id>\d+)/$', views.get_commentall),
    
    url(r'^post-form', views.postform),
    url(r'^comment-form', views.commentform),
    
    url(r'^visitor$', views.visitor, name='visitor'),
    url(r'^visitor/$', views.visitor, name='visitor'),


    url(r'^get-itemsFollow/(?P<username>[a-zA-Z0-9_@\+\-]+)$', views.get_follow),
    url(r'^get-changesFollow/(?P<time>.+)/(?P<username>[a-zA-Z0-9_@\+\-]+)/$', views.get_changeFollow),
    url(r'^get-changesCommentFollow/(?P<time>.+)/(?P<item_id>\d+)/$', views.get_commentchanges),

    url(r'^$', views.home),
]

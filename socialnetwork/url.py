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
from django.conf.urls import url
from django.contrib import admin
from socialnetwork import views
from django.contrib.auth import views as auth_views

urlpatterns = [

    url(r'^register$', views.register,name='register'),
    url(r'^accounts/login/$', auth_views.login,{'template_name':'socialnetwork/log.html'}),
    url(r'^home$', views.home, name='home'),
    url(r'^home/$', views.home, name='home'),
    url(r'^makePost$', views.makePost, name='makePost'),
    url(r'^makePost/$', views.makePost, name='makePost'),
    url(r'^logout$', auth_views.logout_then_login, name='logout'),
    url(r'^visitor$', views.visitor, name='visitor'),
    url(r'^visitor/$', views.visitor, name='visitor'),
    url(r'^myProfile$', views.myProfile, name='myProfile'),
    url(r'^myProfile/$', views.myProfile, name='myProfile'),
    url(r'^otherProfile/(?P<userid>\d+)$', views.otherProfile, name = 'otherProfile'),
    url(r'^otherProfile/(?P<userid>\d+)/$', views.otherProfile, name = 'otherProfile'),
    url(r'^followStream/$', views.followStream, name='followStream'),
    url(r'^followStream$', views.followStream, name='followStream'),
    url(r'^follow/(.*)$', views.follow, name='follow'),
    url(r'^unFollow/(.*)$', views.unFollow, name='unFollow'),
    url(r'^updateProfile/$', views.updateProfile, name='updateProfile'),
    url(r'^updateProfile$', views.updateProfile, name='updateProfile'),
    url(r'^login_to$', views.login_to, name='login_to'),
    url(r'^login_to/$', views.login_to, name='login_to'),
    url(r'^photo/(?P<userid>\d+)$', views.get_photo, name='photo'),
    url(r'^alice/$', views.alice, name='alice'),
    url(r'^$', views.home,name='home'),
]

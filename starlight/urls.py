"""starlight URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
import django.contrib.auth.views
from django.urls import path

from starlight import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('login/', django.contrib.auth.views.login, {'template_name': 'login/login.html'}, name='login'),
    path('logout/', views.logout_view, name='logout'),
    url(r'^(?P<id>\d+)/profile/$', views.profile, name='profile'),
    path('all_profiles/', views.all_profiles, name='all_profiles'),
    url(r'^(?P<employee>\d+)/profile/(?P<id>\d+)/competency/$', views.edit_competency, name='edit_competency'),
    url(r'^(?P<employee>\d+)/profile/new_competency/$', views.new_competency, name='new_competency'),
    path('new_employee/', views.new_employee, name='new_employee'),
    path('teams/', views.view_all_teams, name='teams'),
    url(r'^(?P<id>\d+)/team/$', views.view_team, name='team'),
    path('new_team/', views.new_team, name='new_team'),
    url(r'^(?P<team>\d+)/team/(?P<id>\d+)/remove/$', views.remove_from_team, name='remove_from_team'),
    url(r'^(?P<id>\d+)/team/edit/$', views.edit_team, name='edit_team')
]

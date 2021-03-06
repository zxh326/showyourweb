"""showyourweb URL Configuration

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
from django.contrib import admin
from django.urls import path
from show.views import *
urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('about/', about_view, name='about'),
    path('',index),
    path('auth/reg', register_view, name='reg'),
    path('auth/login', login_view, name='login'),
    path('auth/logout', logout_view, name='logout'),
    path('auth/edit', edit_view, name='edit'),
    path('usr/upload', upload_view, name='upload'),
    path('usr/project', project_view, name='project'),
    path('usr/share', share_view, name='sall'),
    path('usr/share/<str:name>/<str:pname>', share_view, name='share'),
    path('usr/delete', delete_view, name='delete'),
    path('usr/up', up_view, name='up'),


    path('tmp/', test_tmp_view, name='test'),
]

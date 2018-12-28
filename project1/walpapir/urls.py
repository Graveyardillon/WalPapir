"""project1 URL Configuration

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
from django.conf import settings

from . import views
from django.urls import path

from django.conf.urls.static import static

app_name = 'walpapir'

urlpatterns = [

    path('user_d', views.user_d, name='user_d'),
    path('redeem_d', views.redeem_d, name="redeem_d"),

    path('home/', views.home, name='home'),
    path('desktop/', views.desktop, name='desktop'),
    path('mobile/', views.mobile, name='mobile'),
    #userpage and several other pages needs some updates
    path('howToUse/', views.how2use, name='how2use'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('postpage/', views.page4post, name='page4post'),
    path('signup/', views.UserCreate.as_view(), name='signUp'),
    path('signup/done', views.UserCreateDone.as_view(), name='signup_done'),
    path('signup/complete/<token>/', views.UserCreateComplete.as_view(), name='signup_complete'),

]

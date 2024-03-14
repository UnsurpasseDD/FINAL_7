from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.contrib.auth.views import LoginView, LogoutView
from .views import BaseRegisterView, uprade_me, IndexView
from .views import activate, ConfirmUser


urlpatterns = [
    path('login/', 
         LoginView.as_view(template_name = 'sign/login.html'), 
         name='login'),
    path('logout/', 
         LogoutView.as_view(template_name = 'sign/logout.html'), 
         name='logout'),
    path('signup/', 
         BaseRegisterView.as_view(template_name = 'sign/signup.html'), 
         name='signup'),
    path('upgrade/', uprade_me, name='upgrade'),
    path('', IndexView.as_view()),
#     path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/', activate, name='activate'),
    path('confirm/', ConfirmUser.as_view(), name='confirm_user')

]
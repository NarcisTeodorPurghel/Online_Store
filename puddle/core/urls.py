from django.urls import path
from django.contrib.auth import views as auth_views

from . import views #import all views that belongs tot this app

app_name = 'core'
from .forms import LoginForm

urlpatterns = [
    path('', views.index, name='index'),
    path('contact/', views.contact, name='contact'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html',authentication_form=LoginForm), name='login')
]




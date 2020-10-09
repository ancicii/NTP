from django.urls import path
from . import views
from .forms import UserLoginForm
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('', views.home, name="home"),
    path('home/', views.home),
    path('register/', views.register),
    path('login/', LoginView.as_view(authentication_form=UserLoginForm), name='login')
]

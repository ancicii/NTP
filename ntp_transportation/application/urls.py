from django.urls import path
from . import views
from .forms import UserLoginForm
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('register/', views.register, name="register"),
    path('login/', LoginView.as_view(authentication_form=UserLoginForm, redirect_authenticated_user=True), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),

    path('', views.home, name="home"),
    path('home/', views.home),
    path('user/', views.userPage, name="user-page"),

    path('addParcel/', views.add_parcel, name="add-parcel"),
    path('addTrain/', views.add_train, name="add-train"),
    path('addDestination/', views.add_destination, name="add-destination"),
    path('sendParcels/', views.send_parcels, name="add-destination"),
]

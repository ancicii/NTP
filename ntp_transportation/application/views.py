from django.contrib.auth.decorators import permission_required, login_required
from django.shortcuts import render, redirect
from .forms import CreateUserForm, NewParcelForm, NewTrainForm, NewDestinationForm
from django.contrib import messages
from .decorators import unauthenticated_user, allowed_users
from ctypes import *


# Create your views here.

def call_go_function():
    lib = cdll.LoadLibrary("D:\\Faks\\VIII semestar - NTP\\NTP\\ntp_transportation\\application\\main.so")
    # lib.doSearches.argtypes = [c_longlong, c_longlong]
    print(lib.doSearches())


def home(request):
    call_go_function()
    return render(request, 'application/home.html')


@login_required(login_url="login")
@allowed_users(allowed_roles=['ADMIN'])
def add_parcel(request):
    context = {}
    if request.method == "POST":
        form = NewParcelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            context['form'] = form
    else:
        form = NewParcelForm()
        context['form'] = form
    return render(request, 'application/add-parcel.html', context)


@login_required(login_url="login")
@allowed_users(allowed_roles=['ADMIN'])
def add_train(request):
    context = {}
    if request.method == "POST":
        form = NewTrainForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            context['form'] = form
    else:
        form = NewTrainForm()
        context['form'] = form
    return render(request, 'application/add-train.html', context)


@login_required(login_url="login")
@allowed_users(allowed_roles=['ADMIN'])
def add_destination(request):
    context = {}
    if request.method == "POST":
        form = NewDestinationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            context['form'] = form
    else:
        form = NewDestinationForm()
        context['form'] = form
    return render(request, 'application/add-destination.html', context)


@unauthenticated_user
def register(request):
    context = {}
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "User successfully registered! You can log in now!")
            return redirect('login')
        else:
            context['form'] = form
    else:
        form = CreateUserForm()
        context['form'] = form

    return render(request, 'application/register.html', context)


@login_required(login_url="login")
def userPage(request):
    context = {}
    return render(request, 'application/user.html', context)


@login_required(login_url="login")
@allowed_users(allowed_roles=['ADMIN'])
def send_parcels(request):
    context = {}
    return render(request, 'application/send-parcels.html', context)

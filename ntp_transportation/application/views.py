import os
from pathlib import Path

from django.contrib.auth.decorators import permission_required, login_required
import json
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import CreateUserForm, NewParcelForm, NewTrainForm, NewDestinationForm
from django.contrib import messages
from .decorators import unauthenticated_user, allowed_users
from ctypes import *


# Create your views here.
from .models import Parcel


class GoSlice(Structure):
    _fields_ = [("data", POINTER(c_void_p)), ("len", c_longlong), ("cap", c_longlong)]


class GoString(Structure):
    _fields_ = [
        ("p", c_char_p),
        ("n", c_int)]


class Action(Structure):
    _fields_ = [('actionStrings', c_char_p*800)]


def call_go_search_function(request):
    parcels = request.GET.get('parcels', None)
    search = request.GET.get('searchType', None)

    parcel_list = list(map(int, parcels.split(',')))
    dirname = Path(__file__).parent
    rel_path = '../../go_searches/main.so'
    src = (dirname / rel_path).resolve()

    # for i in parcel_list:
    #     edit_parcel = Parcel.objects.get(id=i)
    #     edit_parcel.isDelivered = True
    #     edit_parcel.save()

    lib = cdll.LoadLibrary(str(src))

    lib.doSearches.argtypes = [GoSlice, GoString]
    lib.doSearches.restype = Action

    t = GoSlice((c_void_p * len(parcel_list))(*parcel_list), len(parcel_list), len(parcel_list))
    searchGL = GoString(c_char_p(search.encode('utf-8')), len(search))
    f = lib.doSearches(t, searchGL)
    list_of_found = list()
    for i in f.actionStrings:
        if i is not None:
            list_of_found.append(i.decode('utf-8'))
    write_to_file(list_of_found, search, parcel_list)
    response_data = {'result': 'success', 'message': 'Search done!'}
    return HttpResponse(json.dumps(response_data), content_type="application/json")


def write_to_file(list_of_found, search, parcel_list):
    with open('results.txt', 'a+') as f:
        f.write("parcels: ")
        for item in parcel_list:
            f.write("%s;" % item)
        f.write("\n")
        f.write("search used: %s\n" % str(search))
        f.write("number of actions to goal: %s\n" % len(list_of_found))
        f.write("list of actions: ")
        for item in list_of_found:
            f.write("%s;" % item)
        f.write("\n\n")



def home(request):
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
    obj = Parcel.objects.filter(isDelivered=False)
    context = {'obj': obj}
    return render(request, 'application/send-parcels.html', context)

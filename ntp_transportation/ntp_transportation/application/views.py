from datetime import datetime
from pathlib import Path

from django.conf import settings
from django.contrib.auth.decorators import login_required
import json

from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import CreateUserForm, NewParcelForm, NewTrainForm, NewParcelFormUser
from django.contrib import messages
from .decorators import unauthenticated_user, allowed_users
from ctypes import *
from .models import Parcel, Route, Train, User
from .utils import calculate_distance


class GoSlice(Structure):
    _fields_ = [("data", POINTER(c_void_p)), ("len", c_longlong), ("cap", c_longlong)]


class GoString(Structure):
    _fields_ = [
        ("p", c_char_p),
        ("n", c_int)]


class Action(Structure):
    _fields_ = [('actionStrings', c_char_p * 800)]


def get_routes_to_plot(list_of_found):
    allRoutes = {}
    for action in list_of_found:
        if action.startswith('Travel'):
            trainId = action.split(";")[0].split("_")[1]
            startDestination = action.split(";")[1]
            endDestination = (action.split(";")[2])[:-1]
            if trainId not in allRoutes:
                allRoutes[trainId] = list()
            if startDestination not in allRoutes[trainId]:
                allRoutes[trainId].append(startDestination)
            if endDestination not in allRoutes[trainId]:
                allRoutes[trainId].append(endDestination)

    return allRoutes


def send_email(parcel, type):
    email_from = settings.EMAIL_HOST_USER
    if type == 'shipped':
        subject = "Package has been sent"
        messageSender = "Dear, {} {}. Thank you for choosing our shipping service." \
                        "Your parcel for {} {} has been sent." \
                        "You'll be notified when your shipment arrives at the destination.".format(parcel.senderSurname,
                                                                                                   parcel.senderName,
                                                                                                   parcel.receiverSurname,
                                                                                                   parcel.receiverName)
        subject1 = "Expect package"
        messageReceiver = "Dear, {} {}." \
                          "A parcel for you has been sent.".format(parcel.receiverSurname,
                                                                   parcel.receiverName)
        if parcel.receiver is not None:
            recipient_list_receiver = [parcel.receiver.email, ]
            send_mail(subject1, messageReceiver, email_from, recipient_list_receiver)

        recipient_list = [parcel.sender.email, ]
        send_mail(subject, messageSender, email_from, recipient_list)
    elif type == 'approved':
        subject = "Your package has been approved"
        message = "Dear, {} {}. Thank you for choosing our shipping service." \
                  "Your parcel for {} {} has been approved." \
                  "You'll be notified when we ship it to desired location.".format(parcel.senderSurname,
                                                                                   parcel.senderName,
                                                                                   parcel.receiverSurname,
                                                                                   parcel.receiverName)
        recipient_list = [parcel.sender.email, ]
        send_mail(subject, message, email_from, recipient_list)
    elif type == 'declined':
        subject = "Your package has been declined"
        message = "Dear, {} {}." \
                  "We regret to inform you that your parcel for {} {} has been declined." \
                  "If you have additional questions you can contact us.".format(parcel.senderSurname,
                                                                                parcel.senderName,
                                                                                parcel.receiverSurname,
                                                                                parcel.receiverName)
        recipient_list = [parcel.sender.email, ]
        send_mail(subject, message, email_from, recipient_list)
    elif type == 'received':
        subject = "Your package arrived at the destination"
        message = "Dear, {} {}." \
                  "We are glad to inform you that your parcel for {} {} arrived." \
                  "Thank you for ......".format(parcel.senderSurname,
                                                parcel.senderName,
                                                parcel.receiverSurname,
                                                parcel.receiverName)
        recipient_list = [parcel.sender.email, ]
        send_mail(subject, message, email_from, recipient_list)


@login_required(login_url="login")
@allowed_users(allowed_roles=['ADMIN'])
def call_go_search_function(request):
    search = request.GET.get('searchType', None)
    parcels = request.GET.get('parcels', None)
    parcel_list = list(map(int, parcels.split(',')))
    dirname = Path(__file__).parent
    rel_path = '../../../go_searches/main.so'
    src = (dirname / rel_path).resolve()

    lib = cdll.LoadLibrary(str(src))

    lib.doSearches.argtypes = [GoSlice, GoString]
    lib.doSearches.restype = Action

    t = GoSlice((c_void_p * len(parcel_list))(*parcel_list), len(parcel_list), len(parcel_list))
    searchGL = GoString(c_char_p(search.encode('utf8')), len(search))
    f = lib.doSearches(t, searchGL)
    list_of_found = list()
    for i in f.actionStrings:
        if i is not None:
            list_of_found.append(i.decode('utf8'))
    write_to_file(list_of_found, search, parcel_list)
    all_routes = get_routes_to_plot(list_of_found)
    for i in parcel_list:
        edit_parcel = Parcel.objects.get(id=i)
        edit_parcel.isSent = True
        edit_parcel.dateSent = datetime.now()
        edit_parcel.save()
        if edit_parcel.sender is not None:
            send_email(edit_parcel, 'shipped')

    request.session['all_routes'] = all_routes
    request.session['actions'] = list_of_found
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
            instance = form.save(commit=False)
            instance.price = instance.weight * 0.01 + calculate_distance(instance.destination_from,
                                                                         instance.destination_to) * 0.02
            instance.save()
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
@allowed_users(allowed_roles=['ADMIN'])
def send_parcels(request):
    obj = Parcel.objects.filter(isSent=False) & Parcel.objects.filter(isApproved=True) \
          & Parcel.objects.filter(isDeclined=False)
    context = {'obj': obj}
    return render(request, 'application/send-parcels.html', context)


@login_required(login_url="login")
@allowed_users(allowed_roles=['ADMIN'])
def approve_parcels(request):
    parcelsApprove = request.GET.get('parcelsToApprove', None)
    parcelsDecline = request.GET.get('parcelsToDecline', None)
    if parcelsApprove is not None:
        parcel_list = list(map(int, parcelsApprove.split(',')))
        for i in parcel_list:
            edit_parcel = Parcel.objects.get(id=i)
            edit_parcel.isApproved = True
            edit_parcel.save()
            send_email(edit_parcel, 'approved')
    if parcelsDecline is not None:
        parcel_list = list(map(int, parcelsDecline.split(',')))
        for i in parcel_list:
            edit_parcel = Parcel.objects.get(id=i)
            edit_parcel.isDeclined = True
            edit_parcel.save()
            send_email(edit_parcel, 'declined')

    obj = Parcel.objects.filter(isApproved=False) & Parcel.objects.filter(isSent=False) & Parcel.objects.filter(
        isDeclined=False)
    context = {'obj': obj}
    return render(request, 'application/approve-parcels.html', context)


@login_required(login_url="login")
@allowed_users(allowed_roles=['REGISTERED_USER'])
def send_parcels_user(request):
    context = {}
    typeReq = request.POST.get('type', None)
    if request.method == "POST":
        form = NewParcelFormUser(request.POST)
        form1 = NewParcelFormUser(request.POST)
        if form.is_valid() and typeReq == "address":
            instance = form.save(commit=False)
            instance.senderName = request.user.name
            instance.senderSurname = request.user.surname
            instance.senderContact = request.user.mobile
            instance.destination_from = request.user.city
            instance.sender = request.user
            instance.isApproved = False
            instance.price = instance.weight * 0.01 + calculate_distance(instance.destination_from,
                                                                         instance.destination_to) * 0.02
            instance.save()
            return redirect('my-parcels')
        elif form1.is_valid() and typeReq == "user":
            instance = form1.save(commit=False)
            instance.senderName = request.user.name
            instance.senderSurname = request.user.surname
            instance.senderContact = request.user.mobile
            instance.destination_from = request.user.city
            instance.sender = request.user
            instance.isApproved = False
            instance.receiver = User.objects.get(mobile=instance.receiverContact)
            instance.price = instance.weight * 0.01 + calculate_distance(instance.destination_from,
                                                                         instance.destination_to) * 0.02
            instance.save()
            return redirect('my-parcels')
        else:
            context['form'] = form
            context['form1'] = form1
            context['found'] = False
    else:
        form = NewParcelFormUser()
        form1 = NewParcelFormUser()
        context['form'] = form
        context['form1'] = form1
        context['found'] = False
    return render(request, 'application/send-parcel-user.html', context)


@login_required(login_url="login")
@allowed_users(allowed_roles=['ADMIN'])
def show_result(request):
    all_routes = request.session.get('all_routes', None)
    actions = request.session.get('actions', None)
    routes_to_show = []
    for key in all_routes:
        m = Route(train=Train.objects.get(id=key), destinations=all_routes[key])
        routes_to_show.append(m)
    context = {'all_routes': routes_to_show, 'actions': actions}
    return render(request, 'application/show-result.html', context)


@login_required(login_url="login")
@allowed_users(allowed_roles=['REGISTERED_USER'])
def find_user(request):
    email_phone = request.GET.get('email_phone', None)
    user = User.objects.filter(email=email_phone) | User.objects.filter(mobile=email_phone)

    if user.first() is not None:
        response_data = {'result': list(user.values_list('name', 'surname', 'mobile', 'city')),
                         'message': 'User found!'}
        return HttpResponse(json.dumps(response_data), content_type="json")
    else:
        response_data = {'result': 'fail', 'message': 'User not found!'}
        return HttpResponse(json.dumps(response_data), content_type="json")


@login_required(login_url="login")
@allowed_users(allowed_roles=['REGISTERED_USER'])
def my_parcels(request):
    objSent = Parcel.objects.filter(sender_id=request.user.id)
    objToReceive = Parcel.objects.filter(receiver_id=request.user.id) & Parcel.objects.filter(isApproved=True)
    context = {'objSent': objSent, 'objToReceive': objToReceive}
    return render(request, 'application/my-parcels.html', context)


@login_required(login_url="login")
@allowed_users(allowed_roles=['REGISTERED_USER'])
def set_received(request):
    edit_parcel = Parcel.objects.get(id=request.GET.get("parcelId", None))
    edit_parcel.isDelivered = True
    edit_parcel.save()
    send_email(edit_parcel, 'received')
    return render(request, 'application/my-parcels.html')

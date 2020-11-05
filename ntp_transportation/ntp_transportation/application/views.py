from datetime import datetime, timedelta
from pathlib import Path

from django.conf import settings
from django.contrib.auth.decorators import login_required
import json

from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.html import strip_tags

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
    if type == 'shippedSender':
        subject = 'Your Package Has Been Shipped'
        context = {
            'title': 'Your Package Has Been Shipped',
            'name': "{} {}".format(parcel.senderSurname, parcel.senderName),
            'message': "We want to inform you that a parcel for {} {} has been shipped."
                       "You'll be notified when your shipment arrives at the destination.\n\n"
                       "Thank you for choosing our shipping service.".format(parcel.receiverSurname,
                                                                             parcel.receiverName),
            'delivery_time_from': parcel.dateSent,
            'delivery_time_to': parcel.dateSent + timedelta(days=10),
            'is_delivery': True,
        }
        html_message = render_to_string('application/email.html', context)
        plain_message = strip_tags(html_message)
        recipient_list = [parcel.sender.email, ]
        send_mail(subject, plain_message, email_from, recipient_list, html_message=html_message)
    elif type == 'shippedReceiver':
        subject = 'A Package for You is on its way'
        context = {
            'title': 'A Package for You is on its way',
            'name': "{} {}".format(parcel.receiverSurname, parcel.receiverName),
            'message': "We want to inform you that a parcel from {} {} has been shipped to your address."
                       "Please let us know when you receive it.\n"
                       "Thank you.".format(parcel.senderSurname, parcel.senderName),
            'delivery_time_from': parcel.dateSent,
            'delivery_time_to': parcel.dateSent + timedelta(days=10),
            'is_delivery': True,
        }
        html_message = render_to_string('application/email.html', context)
        plain_message = strip_tags(html_message)
        recipient_list = [parcel.receiver.email, ]
        send_mail(subject, plain_message, email_from, recipient_list, html_message=html_message)

    elif type == 'approved':
        subject = 'Your parcel has been approved'
        context = {
            'title': 'Your parcel has been approved',
            'name': "{} {}".format(parcel.senderSurname, parcel.senderName),
            'message': "We want to inform you that your parcel for {} {} has been approved."
                       "You'll be notified when we ship it to desired location.\n\n"
                       "Thank you for choosing our shipping service.".format(parcel.receiverSurname,
                                                                             parcel.receiverName),
            'delivery_time_from': None,
            'delivery_time_to': None,
            'is_delivery': False,
        }
        html_message = render_to_string('application/email.html', context)
        plain_message = strip_tags(html_message)
        recipient_list = [parcel.sender.email, ]
        send_mail(subject, plain_message, email_from, recipient_list, html_message=html_message)
    elif type == 'declined':
        subject = 'Your parcel has been declined'
        context = {
            'title': 'Your parcel has been declined',
            'name': "{} {}".format(parcel.senderSurname, parcel.senderName),
            'message': "We want to inform you that your parcel for {} {} has been declined.\n\n"
                       "If you have any additional questions please contact us."
                .format(parcel.receiverSurname, parcel.receiverName),
            'delivery_time_from': None,
            'delivery_time_to': None,
            'is_delivery': False,
        }
        html_message = render_to_string('application/email.html', context)
        plain_message = strip_tags(html_message)
        recipient_list = [parcel.sender.email, ]
        send_mail(subject, plain_message, email_from, recipient_list, html_message=html_message)
    elif type == 'received':
        subject = 'Your parcel arrived at its destination'
        context = {
            'title': 'Your parcel arrived at its destination',
            'name': "{} {}".format(parcel.senderSurname, parcel.senderName),
            'message': "We are glad to inform you that your parcel for {} {} arrived.\n\n"
                       "Thank you for choosing our shipping service and we hope you continue to enjoy it!".format(
                parcel.receiverSurname,
                parcel.receiverName),
            'delivery_time_from': None,
            'delivery_time_to': None,
            'is_delivery': False,
        }
        html_message = render_to_string('application/email.html', context)
        plain_message = strip_tags(html_message)
        recipient_list = [parcel.sender.email, ]
        send_mail(subject, plain_message, email_from, recipient_list, html_message=html_message)


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
            send_email(edit_parcel, 'shippedSender')
        if edit_parcel.receiver is not None:
            send_email(edit_parcel, 'shippedReceiver')

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
            instance.price = round((instance.weight * 0.01 + calculate_distance(instance.destination_from,
                                                                         instance.destination_to) * 0.02), 2)
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
            instance.price = round((instance.weight * 0.01 + calculate_distance(instance.destination_from,
                                                                         instance.destination_to) * 0.02), 2)
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
            instance.price = round((instance.weight * 0.01 + calculate_distance(instance.destination_from,
                                                                         instance.destination_to) * 0.02), 2)
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

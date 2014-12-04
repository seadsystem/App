import time
import requests
import re
import ast
import json
from django.http import HttpResponseRedirect, HttpResponse
from seadssite.forms import UserForm, UserProfileForm, PasswordResetRequestForm
from django.template import RequestContext
from django.shortcuts import render, render_to_response
from django.contrib.auth import authenticate, login
from django.views.generic import View, CreateView
from django.core.urlresolvers import reverse
from django.views.generic.base import TemplateView
from django.contrib.auth.models import User
from seadssite.forms import UserForm, UserProfileForm
from .models import Devices, Map
from .helpers import *


from django.core.mail import send_mail
from django.shortcuts import render_to_response as render_to


'''
load main page as "index"
'''
class IndexView(TemplateView):
  template_name = 'index.html'

def help(request, template_name='registration/login.html'):
    # for SMS http://stackoverflow.com/questions/430582/sending-an-sms-to-a-cellphone-using-django
    email = request.POST['email']
    send_mail('Login Information', 'This is a test', 'seadssystems@gmail.com', [email])
    return HttpResponseRedirect('/login')

'''
registration page controller
'''
def register(request):
    #is context needed?
    context = RequestContext(request)
    registered = False

    user_save = request.POST.get('username') or ''
    phone_save = request.POST.get('phone') or ''
    first_name_save = request.POST.get('first_name') or ''
    last_name_save = request.POST.get('last_name') or ''
    email_save = request.POST.get('email') or ''
    cellProvider_save = request.POST.get('cellProvider') or ''
    password_save = request.POST.get('password') or ''

    if request.method == 'POST':
        phone = request.POST['phone']
        cellProvider = request.POST['cellProvider']
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            #Creating a new user
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            # log the user in and send them to the homepage
            registered = True
            user = authenticate (username=request.POST['username'], password=request.POST['password'])
            login(request, user)

            #sending a welcome email to the new user
            #for html/css: http://stackoverflow.com/questions/3237519/sending-html-email-in-django
            toemail = request.POST['email']
            send_mail('Welcome!', 'You are now registered with SEADS.', 'seadssystems@gmail.com', [toemail])

            return HttpResponseRedirect('/')
        #handle invalid form
        else:
            print user_form.errors, profile_form.errors

            # If form is not valid, this would re-render inputtest.html with the errors in the form.
            #render_to_response(request, 'register.html', {'data': 'hello'})
            #why doesn't this line get called on error?
            render_to_response('register.html', {'data': 'hello'})

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render_to_response(
            'register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered, 'user': user_save, 'phone': phone_save, 'first_name':first_name_save, 'last_name':last_name_save, 'email':email_save, 'cell_prov':cellProvider_save, 'password':password_save},
            context)


'''
device dashboard page controller
TODO: users can delete eachothers devices I think
'''
def DashboardView(request):
    alerts = []
    current_user = request.user    
    user_devices_map = Map.objects.filter(user=current_user.id)
    connected_devices = get_connected_devices(user_devices_map)

    #if the user clicked register
    if request.POST.get('register'):
        new_device_id = request.POST.get('device_id')
        new_device_name = request.POST.get('device_name')
        alert = register_device(new_device_id, new_device_name, current_user)
        if alert is not None:
            alerts.append(alert)

    #if the user clicked delete
    elif request.POST.get('delete'):
        device_id = request.POST.get('delete')
        alert = delete_device(device_id, current_user)
        if alert is not None:
            alerts.append(alert)

    return render(request, 'dashboard.html', {'maps': user_devices_map,
     'alerts':alerts, 'connected_devices': connected_devices})


def DevicesView(request):
    alerts = []
    current_user = request.user    
    user_devices_map = Map.objects.filter(user=current_user.id)

    #if the user clicked the editable field and submitted an edit
    if request.POST.get('name') == "modify":
        device_id = request.POST.get('pk')        
        new_name = request.POST.get('value')
        modify_device_name(device_id, new_name)       

    #if the user clicked register
    elif request.POST.get('register'):
        new_device_id = request.POST.get('device_id')
        new_device_name = request.POST.get('device_name')
        alert = register_device(new_device_id, new_device_name, current_user)
        if alert is not None:
            alerts.append(alert)
        
    #if the user clicked delete
    elif request.POST.get('delete'):
        device_id = request.POST.get('delete')
        alert = delete_device(device_id, current_user)
        if alert is not None:
            alerts.append(alert)

    return render(request, 'devices.html', {'maps': user_devices_map, 'alerts':alerts})


def VisualizationView(request, device_id):
    params = request.GET
    start_time = params.get('start_time', 0)
    end_time = params.get('end_time', int(time.time()))
    dtype = params.get('dtype', 'W')
    api_response = get_plug_data(start_time, end_time, dtype, device_id)

    if request.is_ajax():
        return HttpResponse(json.dumps(api_response), content_type="application/json")

    return render(request, 'visualization.html', {'data':api_response})


  

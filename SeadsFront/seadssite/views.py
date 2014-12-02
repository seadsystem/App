import time
import requests
import re
import ast
import json
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render, render_to_response
from django.contrib.auth import authenticate, login
from django.views.generic import View, CreateView
from django.core.urlresolvers import reverse
from django.views.generic.base import TemplateView
from django.contrib.auth.models import User
from seadssite.forms import UserForm, UserProfileForm
from .models import Devices, Map


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
    #get current user and all devices associated via map
    current_user = request.user    
    user_devices_map = Map.objects.filter(user=current_user.id)

    #if the user clicked register
    if request.POST.get('register'):
        #get the new device ID and name from the post
        new_device_id = request.POST.get('device_id')
        new_device_name = request.POST.get('device_name')
        #check if device is already registered to this user
        D = Devices.objects.filter(device_id=new_device_id)
        if Map.objects.filter(user=current_user.id, device=D):
            alerts.append("The device you've attempted to register has already been registered.")
            print "Matching device ID"
        else:
        #try to create a new device and map it to the user
            try:
                D = Devices(device_id=new_device_id, name=new_device_name)
                D.save()     
                Map(user = current_user, device = D).save()
            #catch errors
            except ValueError:
                print "Invalid Device ID"
            except TypeError:
                print "Invalid Device ID"

    #if the user clicked delete
    elif request.POST.get('delete'):
        #get the device ID from the post
        device_id = request.POST.get('delete')
        #get respective DB objects
        D = Devices.objects.filter(device_id = device_id)
        M = Map.objects.filter(device=D)
        #if the user owns the device they are trying to delete
        if Map.objects.filter(user=current_user.id, device=D):
            #if multiple users own the device
            if len(M) > 1:
                #just delete this users map to the device
                Map.objects.filter(user=current_user.id, device=D).delete()
            else:
                #delete the device itself (cascades to map)
                Devices.objects.filter(device_id = device_id).delete()
        else:
            print "you don't own the device you're deleting, or it doesn't exist"


    return render(request, 'dashboard.html', {'maps': user_devices_map, 'alerts':alerts})


def DevicesView(request):
    alerts = []
    #get current user and all devices associated via map
    current_user = request.user    
    user_devices_map = Map.objects.filter(user=current_user.id)
    #if the user clicked the editable field and submitted an edit
    if request.POST.get('name') == "modify":
        #pull info out of request
        device_id = request.POST.get('pk')        
        new_name = request.POST.get('value')        
        '''
        a bit of a hack, this assumes every device has a unique ID, will have to be enforced in DB
        we must also enforce that the name field can't be blank
        '''
        #save info to device object
        D = Devices.objects.filter(device_id = device_id)[0]        
        D.name = new_name
        D.save()
    

    #if the user clicked register
    elif request.POST.get('register'):
        #get the new device ID and name from the post
        new_device_id = request.POST.get('device_id')
        new_device_name = request.POST.get('device_name')
        #check if device is already registered to this user
        D = Devices.objects.filter(device_id=new_device_id)
        if Map.objects.filter(user=current_user.id, device=D):
            alerts.append("The device you've attempted to register has already been registered.")
            print "Matching device ID"
        else:
        #try to create a new device and map it to the user
            try:
                D = Devices(device_id=new_device_id, name=new_device_name)
                D.save()     
                Map(user = current_user, device = D).save()
            #catch errors
            except ValueError:
                print "Invalid Device ID"
            except TypeError:
                print "Invalid Device ID"

    #if the user clicked delete
    elif request.POST.get('delete'):
        #get the device ID from the post
        device_id = request.POST.get('delete')
        #get respective DB objects
        D = Devices.objects.filter(device_id = device_id)
        M = Map.objects.filter(device=D)
        #if the user owns the device they are trying to delete
        if Map.objects.filter(user=current_user.id, device=D):
            #if multiple users own the device
            if len(M) > 1:
                #just delete this users map to the device
                Map.objects.filter(user=current_user.id, device=D).delete()
            else:
                #delete the device itself (cascades to map)
                Devices.objects.filter(device_id = device_id).delete()
        else:
            print "you don't own the device you're deleting, or it doesn't exist"

    #if the user clicked modify
    elif request.POST.get('modify'):
        #get the device ID from the post
        '''
        TODO: Verify that device ID posted for modification is associated with current user
        this avoids sending a post request to modify random peoples devices
        '''
        device_id = request.POST.get('modify')
        #modify the name in the DB
        print "modify the name of device: {}".format(device_id)

    return render(request, 'devices.html', {'maps': user_devices_map, 'alerts':alerts})


'''
workflow:
hit api asking for all data for a device (this gets displayed as soon as the
  user hits the page) then give options for different api calls
'''
def VisualizationView(request, device_id):
    api_string = "http://128.114.59.76:8080/{}".format(device_id)
    api_string += "?type={}".format("W")    
    #print request
    params = request.GET
    start_time = params.get('start_time', 0)
    end_time = params.get('end_time', int(time.time()))
    api_string += "&start_time={}&end_time={}".format(start_time, end_time)
    api_response = requests.get(api_string).text
    api_response = ast.literal_eval(api_response)
    for row in api_response:
        for index, value in enumerate(row):
            if index > 0 and value not in ['I','W']:
                row[index] = int(value)

    s =json.dumps(api_response)
    goodness = json.loads(s)
    print goodness

    if request.is_ajax():
        a = []
        a.append(api_response)
        return HttpResponse(json.dumps(goodness), content_type="application/json")

    return render(request, 'visualization.html', {'data':api_response, 'api_call':api_string})


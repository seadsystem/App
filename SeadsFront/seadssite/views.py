from .models import Devices, Map
from django.http import HttpResponseRedirect, HttpResponse
from seadssite.forms import UserForm, UserProfileForm
from django.template import RequestContext
from django.shortcuts import render, render_to_response
from django.contrib.auth import authenticate, login
from django.views.generic import View, CreateView
from django.core.urlresolvers import reverse
from django.views.generic.base import TemplateView
from django.contrib.auth.models import User


'''
load main page as "index"
'''
class IndexView(TemplateView):
  template_name = 'index.html'


'''
registration page controller
'''
def register(request):
    #is context needed?
    context = RequestContext(request)
    registered = False

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
            return HttpResponseRedirect('/')
        #handle invalid form
        else:
            print user_form.errors, profile_form.errors
    #when method isn't post, show the user a registration form
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render_to_response(
            'register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered},
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

    #if the user clicked device register
    if request.POST.get('register'):
        #get the new device ID and name from the post
        new_device_id = request.POST.get('device_id')
        new_device_name = request.POST.get('device_name')
        #check if device is already registered
        if Devices.objects.filter(device_id=new_device_id):
            '''
            TODO: Deal with this for the user
            '''
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

    #if the user clicked device delete
    elif request.POST.get('delete'):
        #get the device ID from the post
        '''
        TODO: Verify that device ID posted for deletion is associated with current user
        this avoids sending a post request to delete random peoples devices
        '''
        device_id = request.POST.get('delete')
        #delete the record in the DB (cascades to delete the map)
        Devices.objects.filter(device_id = device_id).delete()

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
  api_string = "DB/{}".format(device_id)
  fake_data = [
    ['Time', 'KW/H', 'Temp'],
    ['1',  50,      70],
    ['2',  60,      77],
    ['3',  80,      82],
    ['4',  50,      76],
    ['5',  50,      70],
    ['6',  50,      70],
    ['7',  60,      77],
    ['8',  80,      82],
    ['9',  50,      76],
    ['10',  50,      70],
    ['11',  50,      70],
    ['12',  60,      77],
    ['13',  80,      82],
    ['14',  50,      76],
    ['15',  50,      70],
    ['16',  50,      70],
    ['17',  60,      77],
    ['18',  80,      82],
    ['19',  50,      76],
    ['20',  50,      70]
    ]
  if(request.POST.get('all')):
    api_string = "DB/{}".format(device_id)
    fake_data = [
    ['Time', 'KW/H', 'Temp'],
    ['1',  50,      70],
    ['2',  60,      77],
    ['3',  80,      82],
    ['4',  50,      76],
    ['5',  50,      70],
    ['6',  50,      70],
    ['7',  60,      77],
    ['8',  80,      82],
    ['9',  50,      76],
    ['10',  50,      70],
    ['11',  50,      70],
    ['12',  60,      77],
    ['13',  80,      82],
    ['14',  50,      76],
    ['15',  50,      70],
    ['16',  50,      70],
    ['17',  60,      77],
    ['18',  80,      82],
    ['19',  50,      76],
    ['20',  50,      70]
    ]

  elif(request.POST.get('month')):
    api_string = api_string + "/month"
    fake_data = [
    ['Time', 'KW/H', 'Temp'],
    ['1',  50,      70],
    ['2',  60,      77],
    ['3',  80,      82],
    ['4',  50,      76],
    ['5',  50,      70],
    ['6',  50,      70],
    ['7',  60,      77],
    ['8',  80,      82],
    ['9',  50,      76],
    ['10',  50,      70]
    ]

  elif(request.POST.get('week')):
    api_string = api_string + "/week"
    fake_data = [
    ['Time', 'KW/H', 'Temp'],
    ['1',  50,      70],
    ['2',  60,      77],
    ['3',  80,      82],
    ['4',  50,      76],
    ['5',  50,      70]
    ]

  return render(request, 'visualization.html', {'data':fake_data, 'api_call':api_string})


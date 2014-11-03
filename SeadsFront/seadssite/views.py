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
#from django.shortcuts import render_to_response
#from django.views.generic import CreateView
#from .models import Map

class IndexView(TemplateView):
  template_name = 'index.html'

#Is this used?
def user_login(request):
    context = RequestContext(request)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                #Rango?
                return HttpResponseRedirect('/rango/')
            else:
                #Rango?
                return HttpResponse("Your Rango account is disabled.")
        else:            
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")
    else:
        return render_to_response('rango/login.html', {}, context)

def register(request):
    context = RequestContext(request)
    registered = False
    if request.method == 'POST':

        phone = request.POST['phone']
        cellProvider = request.POST['cellProvider']

        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            # Update our variable to tell the template registration was successful.
            registered = True
            user = authenticate (username=request.POST['username'], password=request.POST['password'])
            login(request, user)
            return HttpResponseRedirect('/')
        #handle invalid form
        else:
            print user_form.errors, profile_form.errors
    #when method isn't post
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render_to_response(
            'register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered},
            context)

def DashboardView(request):
    device_id = 0
    current_user = request.user    
    user_devices = Map.objects.filter(user_id=current_user.id)

    if(request.POST.get('register')):
        new_device_id = request.POST.get('device_id')
        new_device_name = request.POST.get('device_name')
        try:
            D = Devices(device_id=new_device_id, name=new_device_name)
            D.save()     
            Map(user = current_user, device = D).save()
        except ValueError:
            print "Invalid Device ID"
        except TypeError:
            print "Invalid Device ID"

    elif(request.POST.get('delete')):
        device_id = request.POST.get('delete')
        Devices.objects.filter(device_id = device_id).delete()
    
    elif(request.POST.get('modify')):
        print "modify the name of the device"

    return render(request, 'dashboard.html', {'devices': user_devices, 'device_id': device_id})

'''
workflow:
hit api asking for all data for a device (this gets displayed as soon as the
  user hits the page) then give options for different api calls
'''

def VisualizationView(request):
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
    fake_data = [
    ['Time', 'KW/H', 'Temp'],
    ['1',  50,      70],
    ['2',  60,      77],
    ['3',  80,      82],
    ['4',  50,      76],
    ['5',  50,      70]
    ]

  return render(request, 'visualization.html', {'data':fake_data})


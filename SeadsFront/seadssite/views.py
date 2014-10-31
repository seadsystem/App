from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import View
from django.views.generic import CreateView
from django.views.generic.base import TemplateView
from .models import Devices
from .models import Map
from django.contrib.auth.models import User
from seadssite.forms import UserForm, UserProfileForm
from django.template import RequestContext
from django.shortcuts import render_to_response

# Create your views here.
class IndexView(TemplateView):
  template_name = 'index.html'

def user_login(request):
    # Like before, obtain the context for the user's request.
    context = RequestContext(request)

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        username = request.POST['username']
        password = request.POST['password']

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect('/rango/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your Rango account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render_to_response('rango/login.html', {}, context)

def register(request):
    # Like before, get the request's context.
    context = RequestContext(request)

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user

            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to tell the template registration was successful.
            registered = True
            user = authenticate (username=request.POST['username'], password=request.POST['password'])
            login(request, user)
            return HttpResponseRedirect('/')

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print user_form.errors, profile_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
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


from .models import Devices, Map
from django.http import HttpResponseRedirect, HttpResponse
from seadssite.forms import UserForm, UserProfileForm
from django.template import RequestContext
from django.shortcuts import render, render_to_response, get_object_or_404
from django.contrib.auth import authenticate, login
from django.views.generic import View, CreateView
from django.core.urlresolvers import reverse
from django.views.generic.base import TemplateView
from django.contrib.auth.models import User
###Added for blog
from seadssite.models import Blog, Category, newPost
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



class IndexView(TemplateView):
  template_name = 'index.html'


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
        '''
        TODO: Verify that device ID posted for deletion is associated with current user
        this avoids sending a post request to delete random peoples devices
        '''
        device_id = request.POST.get('delete')
        #delete the record in the DB (cascades to delete the map)
        Devices.objects.filter(device_id = device_id).delete()

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

    return render(request, 'dashboard.html', {'maps': user_devices_map})


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




####ADDED for blog

# def WeeklyNews(request):
#     return render_to_response('weeklynews.html',{
#         'categories': Category.objects.all(),
#         'posts': Blog.objects.all()[:5]
#         })

def WeeklyNews(request):
    post_list = Blog.objects.all()
    paginator = Paginator(post_list, 5) # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        post = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)

    return render_to_response('weeklynews.html', {"Blog": Blog})

def view_post(request, slug):
    return render_to_response('viewpost.html',{
        'post':get_object_or_404(Blog, slug=slug)
        })

def view_category(request, slug):
    return render_to_response('viewcategory.html',{
        'category':category,
        'posts': BLog.objects.filter(category=category)[:5]
        })

def post_new(request):
    model = newPost
    return render(request, 'postnew.html') #{'form':form}
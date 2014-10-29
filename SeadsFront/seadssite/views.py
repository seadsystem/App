from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import View
from django.views.generic import CreateView
from django.views.generic.base import TemplateView
from seadssite.forms import UserForm, UserProfileForm
from django.template import RequestContext
from django.shortcuts import render_to_response

# Create your views here.
class IndexView(TemplateView):
  template_name = 'index.html'

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

    # Render the template depending on the context.
    return render_to_response(
            'register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered},
            context)


def VisualizationView(request):
  devices = [1,2,3,4,5]
  fake_data = -1
  if(request.POST.get('all1')):
    fake_data = [
    ['Time', 'KW/H', 'Temp'],
    ['1',  50,      70],
    ['2',  60,      77],
    ['3',  80,      82],
    ['4',  50,      76],
    ['5',  50,      70]
    ]

  return render(request, 'visualization.html', {'data':fake_data, 'devices':devices})
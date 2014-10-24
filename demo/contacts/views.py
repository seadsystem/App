from django.shortcuts import render
from django.views.generic import ListView
from contacts.models import contact
from django.core.urlresolvers import reverse
from django.views.generic import CreateView
from django.http import HttpResponse
from django.views.generic import View
class ListcontactView(ListView):

    model = contact
    template_name = 'contact_list.html'

class CreatecontactView(CreateView):

    model = contact
    template_name = 'edit_contact.html'

    def get_success_url(self):
        return reverse('contacts-list')

class IndexView(View):
	template_name = 'index.html'
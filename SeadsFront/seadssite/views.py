from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.views.generic import View
from django.views.generic import CreateView
from django.views.generic.base import TemplateView

# Create your views here.
class IndexView(TemplateView):
	template_name = 'index.html'
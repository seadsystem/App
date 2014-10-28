from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.views.generic import View
from django.views.generic import CreateView
from django.views.generic.base import TemplateView

# Create your views here.
class IndexView(TemplateView):
	template_name = 'index.html'


def VisualizationView(request):
	fake_data = [
          ['Time', 'KW/H', 'Temp'],
          ['1',  50,      70],
          ['2',  60,      77],
          ['3',  80,      82],
          ['4',  50,      76],
          ['5',  50,      70]
        ]

	return render(request, 'visualization.html', {'data':fake_data})
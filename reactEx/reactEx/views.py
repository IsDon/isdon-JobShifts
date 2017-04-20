from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required

def home(request):

	response = render(request, 'reactEx/front.html')

	return response

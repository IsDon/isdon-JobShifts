from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required

from jobs.views import get_user, base

def home(request, forceadmin=False, userid=None):

	return base(request, forceadmin=forceadmin, userid=userid)

from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import HttpResponse, JsonResponse
from rest_framework.renderers import JSONRenderer
from django.conf import settings
from rest_framework import viewsets
from django.utils import timezone
from django.forms.models import modelformset_factory
from django.core.exceptions import ObjectDoesNotExist


from django.contrib.auth.models import User
from .models import Job, WorkShift, Position
from .serializers import JobSerializer, WorkShiftSerializer, PositionSerializer

# Base Views:
def base(request, forceadmin=False, userid=None):

	u=get_user(request, userid)
	if(u.is_staff):
		forceadmin = True
	
	response = render(request, 'reactEx/front.html', {"forceadmin":forceadmin, "userid":u.id, "name":u.username})

	return response



def latest_set(request):
	return JobList.as_view()(request)


#Allow for mock user id's with custom (DEBUG=True) URLS:
def get_user(request, userid=None):

	u=request.user

	if(settings.DEBUG):
	
		try:
			if(userid):
				u = User.objects.get(pk=userid)
		except User.DoesNotExist:
			pass

	return u




# AJAX functions:

#@login_required	(staff required?)
def PositionOpen(request, pk, userid=None):
	# set a role as <OPEN> (STATUS_POSITION_CHOICES.Open)
	try:
		pos = Position.objects.get(id=pk)
	except Positon.DoesNotExist as e:
		return latest_set(request)

	pos.status = 2
	pos.save()

	return latest_set(request)




from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny


class JobList(generics.ListCreateAPIView):
	permission_classes = (AllowAny,)
	queryset = Job.objects.all()
	serializer_class = JobSerializer

class JobModify(generics.RetrieveUpdateDestroyAPIView):
	permission_classes = (AllowAny,)
	queryset = Job.objects.all()
	serializer_class = JobSerializer

  
class WorkShiftList(generics.ListCreateAPIView):
	permission_classes = (AllowAny,)
	queryset = WorkShift.objects.all()
	serializer_class = WorkShiftSerializer
  
class WorkShiftModify(generics.RetrieveUpdateDestroyAPIView):
	permission_classes = (AllowAny,)
	queryset = WorkShift.objects.all()
	serializer_class = WorkShiftSerializer

  
class PositionList(generics.ListCreateAPIView):
	permission_classes = (AllowAny,)
	queryset = Position.objects.all()
	serializer_class = PositionSerializer
  
class PositionModify(generics.RetrieveUpdateDestroyAPIView):
	permission_classes = (AllowAny,)
	queryset = Position.objects.all()
	serializer_class = PositionSerializer

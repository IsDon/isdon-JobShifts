from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import HttpResponse, JsonResponse
from rest_framework.renderers import JSONRenderer
from rest_framework import viewsets
from django.utils import timezone
from django.forms.models import modelformset_factory
from django.core.exceptions import ObjectDoesNotExist


from .models import Job, WorkShift, Position
from .serializers import JobSerializer, WorkShiftSerializer, PositionSerializer

# Base Views:
def home(request):

	response = render(request, 'reactEx/front.html')

	return response


def latest_set(request):

	return JobList.as_view()(request)



# Day layout:

# def daily(request):

# 	response = render(request, 'reactEx/dayview.html')

# 	return response





# AJAX functions:
# from rest_framework.filters import OrderingFilter

# class JobListViewSet(viewsets.ModelViewSet):
# 	queryset = Job.objects.all()
# 	serializer_class = JobSerializer
# 	filter_backends = (OrderingFilter,)
# 	ordering_fields = ('username', 'email')

#@login_required	(staff required?)
def PositionOpen(request, pk):
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

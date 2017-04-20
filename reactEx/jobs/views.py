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


# Day layout:

def daily(request):

	response = render(request, 'reactEx/dayview.html')

	return response





# AJAX functions:
from rest_framework.filters import OrderingFilter

class JobListViewSet(viewsets.ModelViewSet):
	queryset = Job.objects.all()
	serializer_class = JobSerializer
	filter_backends = (OrderingFilter,)
	ordering_fields = ('username', 'email')



# from .forms import AddJobForm

# def AddJob(request):

# 	if request.method == 'POST':

# 		print(request.POST)
# 		form = AddJobForm(request.POST or None)

# 		if form.is_valid():
# 			print('*****Saving*****')
# 			form.save()
# 		else:
# 			print(form.errors)
	
# 	# jobList = Job.objects.all()
# 	# print(len(jobList))
# 	# if(not jobList):
# 	# 	print('Empty Job List')
# 	# 	jsonJobs = []	# match empty set in format below TODO
# 	# else:
# 	# 	serializedJobs = JobSerializer(jobList)
# 	# 	print(serializedJobs.data)
# 	# 	jsonJobs = JSONRenderer().render(serializedJobs.data)

# 	#response = JobListViewSet.list(AddJob, request)
# 	response = JobList.as_view()
# 	print(response)
# 	return response
# 	# return JsonResponse({
# 	# 	"response" 	: "success",
# 	# 	# "html_list"	: render_to_string(
# 	# 	# 	'reactEx/dayview.html', {
#  #  #           }, 
#  #  #           request=request
#  #  #       ),
# 	# 	"jobs"		: jsonJobs
#  #    })




from rest_framework import generics


class JobList(generics.ListCreateAPIView):
	queryset = Job.objects.all()
	serializer_class = JobSerializer

class JobModify(generics.RetrieveUpdateDestroyAPIView):
	queryset = Job.objects.all()
	serializer_class = JobSerializer
  
class WorkShiftList(generics.ListCreateAPIView):
	queryset = WorkShift.objects.all()
	serializer_class = WorkShiftSerializer
  
class PositionList(generics.ListCreateAPIView):
	queryset = Position.objects.all()
	serializer_class = PositionSerializer

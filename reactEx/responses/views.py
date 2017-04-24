from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.contrib.auth.decorators import login_required

from jobs.models import Job, WorkShift, Position
from jobs.choices import *
from .models import Response

# Responses to Shift Position openings (sent out by Admin)


def latest_set(request):
	# for user, return jobs, shifts, positions open OR user.accepted:
	# u = request.user

	# filterPositions = Position.object.filter(staff=u).filter(status__in=STATUS_POSITION_VISIBLE)
	# print(filterPositions)

	# filterWorkShifts = WorkShift.objects.filter(ShiftPosition__in=filterPositions)
	# queryset = Job.objects.filter(JobShift__in=filterWorkShifts)
	# serializer_class = JobSerializer
	return ResponseJobList.as_view()(request)

# AJAX views:
def PositionAccept(request, pk):

	# accept response - add new response(user, position=pk):
	try:
		pos = Position.objects.get(id=pk)
	except Positon.DoesNotExist as e:
		return latest_set(request)

	req = Response.objects.create(position=pos, staff=request.user, status=3, message="default")

	return latest_set(request)

def PositionRevoke(request, pk):

	return latest_set(request)




from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny

from jobs.serializers import JobSerializer, WorkShiftSerializer, PositionSerializer
from jobs.serializers import filteredJobSerializer, filteredResponseSerializer, filteredPositionSerializer

class ResponseJobList(generics.ListAPIView):
	permission_classes = (AllowAny,)
	serializer_class = filteredJobSerializer
	queryset = Job.objects.all()

	def get_queryset(self):
		"""
	# for user, return jobs, shifts, positions open OR user.accepted:
		"""
		user = self.request.user
		filterPositions = Position.objects.filter(staff_filling_id=user.id).filter(
			status__in=STATUS_POSITION_VISIBLE)
		filterWorkShifts = WorkShift.objects.filter(ShiftPosition__in=filterPositions)
		return Job.objects.filter(JobShift__in=filterWorkShifts)
		# filterPositions = Position.objects.filter(staff_filling_id=user.id).filter(
		# 	status__in=STATUS_POSITION_VISIBLE)

		# return Response.objects.filter(position__in=filterPositions)

	# Shift view not implemented:
# class ResponseWorkShiftList(generics.ListCreateAPIView):
# 	permission_classes = (AllowAny,)
# 	queryset = WorkShift.objects.all()
# 	serializer_class = WorkShiftSerializer

class ResponsePositionList(generics.ListAPIView):
	permission_classes = (AllowAny,)
	queryset = Position.objects.filter(status__in=STATUS_POSITION_VISIBLE)
	serializer_class = filteredPositionSerializer

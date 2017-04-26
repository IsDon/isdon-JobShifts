from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from jobs.models import Job, WorkShift, Position
from jobs.choices import *
from .models import Response
from jobs.views import get_user

import logging
logger = logging.getLogger("django")

# Responses to Shift Position openings (sent out by Admin)


def latest_set(request, userid=None):
	return ResponseJobList.as_view()(request, userid=userid)

# AJAX views:
def PositionAccept(request, pk, userid=None):
	# accept response - add new response(user, position=pk, status=AVAILABLE):
	
	STATUS = 3
	try:
		pos = Position.objects.get(id=pk)
	except Position.DoesNotExist as e:
		return latest_set(request, userid=userid)

	u=get_user(request, userid)
	try:
		req = Response.objects.get(position=pos, staff=u)
		req.status=STATUS
		req.save()
	except Response.DoesNotExist as e:
		req = Response.objects.create(position=pos, staff=u, status=STATUS, message="default")

	return latest_set(request, userid=userid)


def PositionRevoke(request, pk, userid=None):
	# remove acceptance response - add new response(user, position=pk, status=UNAVAILABLE):
	
	STATUS = 4
	try:
		req = Response.objects.get(id=pk)
		if(req.status==STATUS):
			req.delete()
		else:
			req.status=STATUS
			req.save()
	except Response.DoesNotExist as e:
		print('No Response found in Revoke')
		print(str(e))

		u=get_user(request, userid)
		req = Response.objects.create(position=pos, staff=u, status=STATUS, message="default")

	return latest_set(request, userid=userid)




from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny

from jobs.serializers import JobSerializer, WorkShiftSerializer, PositionSerializer
from jobs.serializers import filteredJobSerializer, filteredResponseSerializer, filteredPositionSerializer

class ResponseJobList(generics.ListAPIView):
	permission_classes = (AllowAny,)
	serializer_class = filteredJobSerializer
	queryset = Job.objects.all()
	# additional named parameters for passing as_view call:
	userid = None
	user = None

	def get_serializer_context(self):
		if(self.userid):
			userid = self.userid
		if(self.kwargs['userid']):
			userid = self.kwargs['userid']
		u=get_user(self.request, userid)
		queryset = self.queryset
		return {
			'request': self.request,
			#'format': self.format_kwarg,
			'format': {'user':u},
			'view': self
		}
		#return {"userid": self.userid, "user": u}

	def get_queryset(self):
		"""
	# for user, return jobs, shifts, positions open OR user.accepted:
		"""
		if(self.userid):
			userid = self.userid
		if(self.kwargs['userid']):
			userid = self.kwargs['userid']
		u=get_user(self.request, userid)
		filterPositions = Position.objects.filter(Q(staff_filling_id=u.id) | Q(
			status__in=STATUS_POSITION_VISIBLE))
		filterWorkShifts = WorkShift.objects.filter(ShiftPosition__in=filterPositions)
		return Job.objects.filter(JobShift__in=filterWorkShifts)

	# Shift view not implemented:
# class ResponseWorkShiftList(generics.ListCreateAPIView):
# 	permission_classes = (AllowAny,)
# 	queryset = WorkShift.objects.all()
# 	serializer_class = WorkShiftSerializer

# class ResponsePositionList(generics.ListAPIView):
# 	permission_classes = (AllowAny,)
# 	queryset = Position.objects.filter(status__in=STATUS_POSITION_VISIBLE)
# 	serializer_class = filteredPositionSerializer

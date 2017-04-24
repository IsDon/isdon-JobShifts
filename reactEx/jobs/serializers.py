from rest_framework import serializers
from rest_framework.filters import OrderingFilter
from django.db.models import Q

from .models import Job, WorkShift, Position
from .choices import STATUS_POSITION_VISIBLE
from responses.models import Response

class ResponseSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = Response
		fields = ('id', 'position', 'status', 'get_status_display', 'staff', 'staff_name', 'message')
		url = 'response'

class PositionSerializer(serializers.ModelSerializer):
	subList = ResponseSerializer(many=True, source='ResponsePosition', read_only=True)
	
	class Meta:
		model = Position
		fields = ('id', 'workShift', 'role', 'status', 'get_status_display', 'staff_filling', 'subList')
		url = 'role'


class WorkShiftSerializer(serializers.ModelSerializer):
	subList = PositionSerializer(many=True, source='ShiftPosition', read_only=True)
	
	class Meta:
		model = WorkShift
		fields = ('id', 'job', 'time_start', 'time_end', 'subList')
		url = 'shift'


class JobSerializer(serializers.ModelSerializer):
	subList = WorkShiftSerializer(many=True, source='JobShift', read_only=True)

	class Meta:
		model = Job
		fields = ('id', 'name', 'desc', 'location', 'subList')


# Add a filter for Contractors to only see relevent data to themself (user) and open slots:
class FilteredResponseListSerializer(serializers.ListSerializer):

	def to_representation(self, data):
		user = self.context['request'].user
		data = data.filter(
			Q(staff_id=user.id)
		)
		return super(FilteredResponseListSerializer, self).to_representation(data)

class FilteredPositionListSerializer(serializers.ListSerializer):

	def to_representation(self, data):
		user = self.context['request'].user
		data = data.filter(
			Q(staff_filling_id=user.id) | 
			Q(status__in=STATUS_POSITION_VISIBLE)
		)
		return super(FilteredPositionListSerializer, self).to_representation(data)

# Inherit Serializers, override chain to pass a new set of (filtered) nested lists:
class filteredResponseSerializer(ResponseSerializer):
	class Meta(ResponseSerializer.Meta):
		list_serializer_class = FilteredResponseListSerializer


class filteredPositionSerializer(PositionSerializer):
	subList = filteredResponseSerializer(many=True, source='ResponsePosition', read_only=True)
	class Meta(PositionSerializer.Meta):
		list_serializer_class = FilteredPositionListSerializer


class filteredWorkShiftSerializer(WorkShiftSerializer):
	subList = filteredPositionSerializer(many=True, source='ShiftPosition', read_only=True)



class filteredJobSerializer(JobSerializer):
	subList = filteredWorkShiftSerializer(many=True, source='JobShift', read_only=True)


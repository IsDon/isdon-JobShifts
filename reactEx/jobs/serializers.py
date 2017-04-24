from rest_framework import serializers
from rest_framework.filters import OrderingFilter

from .models import Job, WorkShift, Position
from .choices import STATUS_POSITION_VISIBLE
from responses.models import Response

class ResponseSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = Response
		fields = ('id', 'position', 'status', 'get_status_display', 'staff', 'staff__name', 'message')
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



class FilteredPositionListSerializer(serializers.ListSerializer):

	def to_representation(self, data):

		data = data.filter(status=2) #.filter(status__in=STATUS_POSITION_VISIBLE)#.filter(staff_filling_id=self.context['request'].user.id)
		return super(FilteredPositionListSerializer, self).to_representation(data)


class filteredResponseSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = Response
		fields = ('id', 'position', 'status', 'get_status_display', 'staff', 'staff__name', 'message')
		url = 'response'


class filteredPositionSerializer(serializers.ModelSerializer):
	subList = filteredResponseSerializer(many=True, source='ResponsePosition', read_only=True)
	
	class Meta:
		model = Position
		fields = ('id', 'workShift', 'role', 'status', 'get_status_display', 'staff_filling', 'subList')
		url = 'role'
		list_serializer_class = FilteredPositionListSerializer


class filteredWorkShiftSerializer(serializers.ModelSerializer):
	subList = filteredPositionSerializer(many=True, source='ShiftPosition', read_only=True)
	
	class Meta:
		model = WorkShift
		fields = ('id', 'job', 'time_start', 'time_end', 'subList')
		url = 'shift'


class filteredJobSerializer(serializers.ModelSerializer):
	subList = filteredWorkShiftSerializer(many=True, source='JobShift', read_only=True)

	class Meta:
		model = Job
		fields = ('id', 'name', 'desc', 'location', 'subList')


from rest_framework import serializers
from rest_framework.filters import OrderingFilter

from .models import Job, WorkShift, Position

class PositionSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = Position
		fields = ('id', 'workShift', 'role', 'status', 'staff_filling')
		url = 'role'


class WorkShiftSerializer(serializers.ModelSerializer):
	subList = PositionSerializer(many=True, source='Shift_Position', read_only=True)
	
	class Meta:
		model = WorkShift
		fields = ('id', 'job', 'time_start', 'time_end', 'subList')
		url = 'shift'


class JobSerializer(serializers.ModelSerializer):
	subList = WorkShiftSerializer(many=True, source='Job_Shift', read_only=True)

	class Meta:
		model = Job
		fields = ('id', 'name', 'desc', 'location', 'subList')


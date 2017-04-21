from django.conf import settings
from django.db import models

from django.contrib.auth.models import User
from .choices import *

# Models for Job / Shifts / Positions to be filled

class Job(models.Model):

	name = 			models.CharField(db_index=True, unique=False, max_length=40)
	desc = 			models.TextField(db_index=False, blank=True, null=True)
	location = 		models.CharField(db_index=True, unique=False, blank=True, null=True, max_length=100)

	def __str__(self):
		if(self.location):
			return "%s (%s)" % (self.name, self.location)
		else:
			return self.name

class WorkShift(models.Model):

	job = models.ForeignKey( Job, 
		db_index=True,
        related_name="Job_Shift",
        related_query_name="Job_Shift",
        null=False,
        on_delete=models.CASCADE)
	time_start =  	models.DateTimeField(db_index=True, unique=False)
	time_end = 	 	models.DateTimeField(db_index=True, unique=False)

	def __str__(self):
		return "%s - %s" % (self.time_start, self.time_end)

class Position(models.Model):

	workShift = models.ForeignKey( WorkShift, 
		db_index=True,
		related_name="Shift_Position",
		related_query_name="Shift_Position",
		null=False,
		on_delete=models.CASCADE)
	role =			models.CharField(db_index=True, unique=False, max_length=20)
	status = 		models.IntegerField(choices=STATUS_POSITION_CHOICES, default=1)
	staff_filling = models.ForeignKey( User, 
		db_index=True,
		related_name="StaffedBy",
		related_query_name="StaffedBy",
		null=True, 
		on_delete=models.SET_NULL)

	def __str__(self):
		return "%s - %s" % (self.role, self.StaffedBy.name)
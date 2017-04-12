from django.conf import settings
from django.db import models

from choices import *

# Models for Job / Shifts / Positions to be filled

class Job(models.Model):

	name = 			models.CharField(db_index=True, unique=False, max_length=40)
	desc = 			models.TextField(db_index=False)
	location = 		models.CharField(db_index=True, unique=False, max_length=100)

class Shift(models.Model):

	job = 			models.ForeignKey(Job, db_index=True,
        related_name="Job_Shift",
        related_query_name="Job_Shift",
        null=False,
        on_delete=models.CASCADE)
	time_start =  	models.DateTimeField(db_index=True, unique=False)
	time_end = 	 	models.DateTimeField(db_index=True, unique=False)

class Position(models.Model):

	shift = 		models.ForeignKey(Shift, db_index=True,
		related_name="Shift_Position",
		related_query_name="Shift_Position",
		null=False,
		on_delete=models.CASCADE)
	role =			models.CharField(db_index=True, unique=False, max_length=20)
	status = 		models.IntegerField(choices=STATUS_POSITION_CHOICES, default=1)
	staff_filling = models.ForeignKey(User, Null=True, on_delete=models.SET_NULL)

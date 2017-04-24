from django.conf import settings
from django.db import models

from django.contrib.auth.models import User
from jobs.choices import *
from jobs.models import Position

# Contractor / Casual Staff Responses to Shift Openings

class Response(models.Model):

	position = models.ForeignKey( Position, 
		db_index=True,
		related_name="ResponsePosition",
		related_query_name="ResponsePosition",
		null=False,
		on_delete=models.CASCADE)
	status = 		models.IntegerField(choices=STATUS_RESPONSE_CHOICES, default=1)
	message = 		models.TextField(max_length=500, blank=True)
	staff = models.ForeignKey( User, 
		db_index=True,
		related_name="StaffResponse",
		related_query_name="StaffResponse",
		null=True, 
		on_delete=models.SET_NULL)

	def __str__(self):
		return "%s" % (self.role)
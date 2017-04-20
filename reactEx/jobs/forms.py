from django import forms
from django.views.decorators.csrf import csrf_exempt

from .models import Job, WorkShift, Position



# class AddJobForm(forms.ModelForm):
	
# 	name = forms.CharField(max_length=20, help_text="Please enter a job Name")
# 	location = forms.CharField(max_length=20, required=False, help_text="Please enter a main location")

# 	class Meta:
# 		model = Job
# 		fields = ('name', 'location', )

from django.test import TestCase
from django.db import IntegrityError

# Model Logic:

from .models import *

class BasicDataTestCase(TestCase): 
	@classmethod
	def setUpTestData(self):   	#state rolled back to after each test
		self.user = User.objects.create_user(
			username='user', 
			email='user@123.com', 
			password='top_secret'
			)
		self.stdJobName = "Asteroid Drilling"
		self.stdJobDesc = "-"
		self.stdJobLoc = "3rd star on the left"
		self.stdShiftTimeStart = "2017-05-01 08:00+10:00"
		self.stdShiftTimeEnd = "2017-05-01 17:30+10:00"
		self.stdPositionRole = "Redshirt"

	def setUp(self):			#run before each test from scratch
		pass

	def test_new_Job_allowsCreate_Shift(self):
		newJob = Job.objects.create(
			name=self.stdJobName,
			desc=self.stdJobDesc,
			location=self.stdJobLoc
			)

		with self.assertRaises(IntegrityError):
			newShift= WorkShift.objects.create(
				time_start=self.stdShiftTimeStart,
				time_end=self.stdShiftTimeEnd
				)
			print(newShift)

		newShift2= Shift(
			job=newJob,
			time_start=self.stdShiftTimeStart,
			time_end=self.stdShiftTimeEnd
			)
		self.assertTrue(
			newShift2
			)




# Userena + extended user model (one-to-one):

from userena.forms import SignupForm
from userena.tests.tests_forms import SignupFormTests
from userena.models import UserenaSignup

class FormTests(SignupFormTests):
    def setUp(self):
        # Setup userena permissions
        UserenaSignup.objects.check_permissions()

    def test_validation(self):
        form_data = {
            'username': 'X' * 300,
            'email': 'X' * 300,
            'password1': 'X' * 300,
        }
        form = SignupForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_blank_data(self):
        form = SignupForm({})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'username': ['This field is required.'],
            'email': ['This field is required.'],
            'password1': ['This field is required.'],
            'password2': ['This field is required.'],
        })


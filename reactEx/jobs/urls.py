from django.conf.urls import include, url
from . import views

urlpatterns = [
	# base url
    url(r'^$', views.base, name='jobs_home'),
    
    # Day View:
    #url(r'^daily/(?P<day_ts>\d{4}-\d{2}-\d{2})/$', views.daily, name='jobs_daily'),
    #url(r'^daily/(?P<dev_id>[0-9]+)/daily/(?P<day_ts>NEXT)/$', views.daily, name='jobs_daily_nextavail'),



	# AJAX API:

	url(r'^api/$', views.JobList.as_view(), name='jobs-base'),		#list (GET), add (POST)
	url(r'^api/id/$', views.JobList.as_view()),		#list (GET), add (POST)
	url(r'^api/job/$', views.JobList.as_view(), name='jobs-list'),		#list (GET), add (POST)
	url(r'^api/shift/$', views.WorkShiftList.as_view(), name='shifts-list'),		#list (GET), add (POST)
	url(r'^api/role/$', views.PositionList.as_view(), name='roles-list'),		#list (GET), add (POST)
	#url(r'^api/add/$', views.AddJob, name='add-job'),
	url(r'^api/job/(?P<pk>[0-9]+)/$', views.JobModify.as_view(), name='mod-job'),	#delete (DELETE), update (PUT), partial_update (PATCH), get (GET)
	url(r'^api/shift/(?P<pk>[0-9]+)/$', views.WorkShiftModify.as_view(), name='mod-shift'),	#delete (DELETE), update (PUT), partial_update (PATCH), get (GET)
	url(r'^api/role/(?P<pk>[0-9]+)/$', views.PositionModify.as_view(), name='mod-role'),	#delete (DELETE), update (PUT), partial_update (PATCH), get (GET)
	
	url(r'^api/role/open/(?P<pk>[0-9]+)/$', views.PositionOpen, name='open-role'),	#delete (DELETE), update (PUT), partial_update (PATCH), get (GET)



    # Week View, etc:

]
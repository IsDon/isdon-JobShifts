from django.conf.urls import include, url
from . import views

urlpatterns = [
	# base url
    url(r'^$', views.home, name='jobs_home'),
    
    # Day View:
    url(r'^daily/(?P<day_ts>\d{4}-\d{2}-\d{2})/$', views.daily, name='jobs_daily'),
    url(r'^daily/(?P<dev_id>[0-9]+)/daily/(?P<day_ts>NEXT)/$', views.daily, name='jobs_daily_nextavail'),



	# AJAX API:

	url(r'^api/$', views.JobList.as_view(), name='daily-list'),		#list (GET), add (PUT)
	#url(r'^api/add/$', views.AddJob, name='add-job'),
	url(r'^api/id/(?P<pk>[0-9]+)/$', views.JobModify.as_view(), name='mod-job'),	#delete (DELETE), update (PUT), partial_update (PATCH), get (GET)



    # Week View, etc:

]
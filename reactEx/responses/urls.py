from django.conf.urls import include, url

from jobs import views as jobviews
from . import views

urlpatterns = [
	# base url
    url(r'^$', jobviews.base),
    


	# AJAX API:

	url(r'^api/$', views.ResponseJobList.as_view(), name='responses-base'),		#list (GET), add (POST)

	url(r'^api/accept/(?P<pk>[0-9]+)/$', views.PositionAccept, name='propose-role'),	#delete (DELETE), update (PUT), partial_update (PATCH), get (GET)
	url(r'^api/revoke/(?P<pk>[0-9]+)/$', views.PositionRevoke, name='revoke-role'),	#delete (DELETE), update (PUT), partial_update (PATCH), get (GET)
]

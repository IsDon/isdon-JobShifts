"""reactEx URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.sites.models import Site

from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^forceadmin/$', views.home, {'forceadmin': 'true'}, name='force_admin'),


    # Staffer Views:
    url(r'^responses/', include('responses.urls')),
    url(r'^forceadmin/responses/', include('responses.urls')),
    # Admin (Business Owner) Additional Views:
    url(r'^jobs/', include('jobs.urls')),
    url(r'^forceadmin/jobs/', include('jobs.urls')),



    # AJAX functions:



    # django.js includes:
    url(r'^djangojs/', include('djangojs.urls')),


    # admin site (DJango):
    url(r'^admin/', admin.site.urls),

    # insert userena overrides if required:

    # base userena:
    url(r'^accounts/', include('userena.urls')),
]

#windows environment static server:
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()

admin.autodiscover()
admin.site.unregister(Site)
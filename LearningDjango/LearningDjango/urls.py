"""
Definition of urls for LearningDjango.
"""

from datetime import datetime
from django.conf.urls import include, url
import django.contrib.auth.views

import HelloDjangoApp.views

# Django processes URL patterns in the order they appear in the array
urlpatterns = [
    url(r'^$', HelloDjangoApp.views.index, name='index'),
    url(r'^home$', HelloDjangoApp.views.index, name='home'),
    url(r'^about$', HelloDjangoApp.views.about, name='about'),
]
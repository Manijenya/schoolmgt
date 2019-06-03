"""
Dashbaord URL Configure
"""
from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', TeacherView.as_view(), name="teacher_page"),
    url(r'^student_list/$', student_list, name="student_list"),
  ]

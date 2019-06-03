# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django import forms
from .models import SubjectDetails, StudentDetails, TeacherDetails

# Register your models here.

admin.site.register(SubjectDetails)
#admin.site.register(MarkDetails)
admin.site.register(StudentDetails)
admin.site.register(TeacherDetails)
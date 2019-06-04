# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging, json, string
import logging.handlers
from django.shortcuts import render,redirect,reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.db import connection
from .models import *
logger_obj = logging.getLogger('logit')


class TeacherView(View):
    ''' 
    02-Jun-2019 To Teacher page loaded.
    @param request: Request Object
    @type request : Object
    @return:   HttpResponse or Redirect the another URL
    @author: MKM
    '''
    template_name = "teacher/teacher.html"
     
    def get(self, request, *args, **kwargs):
        # if request.user.is_authenticated():
        cur = connection.cursor()
        if request.user.is_authenticated:
            cur = connection.cursor()
            cur.execute("""SELECT sd.id, sd.subject_name, sd.subject_code FROM subject_details sd inner join teacher_details td on td.teacher_subject_id = sd.id 
            inner join  auth_user au on au.id = td.teacher_name_id and au.username = %s""", (str(request.user.username),))
            role_data= dictfetchall(cur)
            return render(request, self.template_name, {'role_data':role_data})
        else:
            return HttpResponseRedirect('/')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(TeacherView, self).dispatch(request, *args, **kwargs)
    
@csrf_exempt
def student_list(request):
    cur = connection.cursor()   
    json_data = {}
    try:
        if request.method == 'GET':
            cur.execute("""SELECT sd.id, sd.subject_name, sd.subject_code FROM subject_details sd inner join teacher_details td on td.teacher_subject_id = sd.id 
            inner join  auth_user au on au.id = td.teacher_name_id and au.username = %s""", (str(request.user.username),))
            role_data= dictfetchall(cur)
            cur.execute("select subject_name, subject_code from subject_details order by id")
            subject_data= dictfetchall(cur)
            cur.execute("""select sd.subject_name, md.mark, md.student_id_id from subject_details sd  inner join mark_details md on md.subject_id_id = sd.id 
            order by md.student_id_id""")
            mark_data = dictfetchall(cur)
            cur.execute("select id, student_name from student_details order by id")
            student_data= dictfetchall(cur)
            cur.execute("select id, student_name , student_total from student_details order by student_total desc")
            rank_data= dictfetchall(cur)
            json_data['role_data'] = role_data
            json_data['subject'] = subject_data
            json_data['students'] = student_data
            json_data['rank'] = rank_data
            json_data['status'] = 'Success'
    except Exception as e:
        print "----------",e
        logger_obj.info("Sudent Details "+ str(e) +" attempted by "+str(request.user.username))
        json_data["status"] = 'Error'
    return HttpResponse(json.dumps(json_data))

def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict."
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()]
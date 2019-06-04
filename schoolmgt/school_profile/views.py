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
    03-Jun-2019 To Teacher page loaded.
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
#             cur.execute("""SELECT au.username, sd.id, sd.subject_name, sd.subject_code FROM subject_details sd inner join teacher_details td on td.teacher_subject_id = sd.id 
#             inner join  auth_user au on au.id = td.teacher_name_id and au.username = %s""", (str(request.user.username),))
#             role_data= dictfetchall(cur)
#             print "-----------",role_data
            return render(request, self.template_name, {'role_data':request.user.username})
        else:
            return HttpResponseRedirect('/')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(TeacherView, self).dispatch(request, *args, **kwargs)
    
@csrf_exempt
def student_list(request):
    ''' 
    04-Jun-2019 To Studen list, rank data and subject page loaded.
    @param request: Request Object
    @type request : Object
    @return:   HttpResponse or Redirect the another URL
    @author: MKM
    '''
    cur = connection.cursor()   
    json_data = {}
    print "-asdfasdasd",request.method

    try:
        if request.method == 'GET':
            cur.execute("""SELECT au.username, sd.id, sd.subject_name, sd.subject_code FROM subject_details sd inner join teacher_details td on td.teacher_subject_id = sd.id 
            inner join  auth_user au on au.id = td.teacher_name_id and au.username = %s""", (str(request.user.username),))
            role_data= dictfetchall(cur)
            cur.execute("select subject_name, subject_code from subject_details order by id")
            subject_data= dictfetchall(cur)
            cur.execute("""select sd.subject_name, md.mark, md.student_id_id ,md.subject_id_id from subject_details sd  inner join mark_details md on md.subject_id_id = sd.id 
            order by md.student_id_id""")
            mark_data = dictfetchall(cur)
            cur.execute("select id, student_name from student_details order by id")
            student_data= dictfetchall(cur)
            cur.execute("select id, student_name , student_total, student_pass_fail from student_details order by student_total desc")
            rank_data= dictfetchall(cur)
            json_data['role_data'] = role_data
            json_data['subject'] = subject_data
            json_data['students'] = student_data
            json_data['rank'] = rank_data
            json_data['mark_data'] = mark_data
            json_data['status'] = 'Success'
            
        elif request.method == 'POST':
            cur.execute("select subject_name, subject_code from subject_details order by id")
            subject_data= dictfetchall(cur)
            data = request.POST.get('datas')
            data = json.loads(data)
            subject_len = int(len(subject_data))
            student_len = int(data['student_len'])
            cur.execute("delete from mark_details")
            for i in range(student_len):
                temp_total = 0
                pass_fail = True
                for j in range(subject_len):
                    mark = data[subject_data[j]['subject_name']+str(j)+'_'+str(i+1)]
                    if int(mark) < 35:
                        pass_fail = False
                    temp_total = temp_total + int(mark)
                    cur.execute(""" INSERT INTO mark_details(mark, student_id_id, subject_id_id) VALUES(%s, %s, %s)""",
                                ( int(mark), (i+1), (j+1), ))
                cur.execute(""" update student_details set student_total = %s, student_pass_fail = %s where id = %s""",
                                ( int(temp_total), pass_fail, (i+1),))
            json_data['status'] = 'Success'
    except Exception as e:
        print "----------",e
        logger_obj.info("Sudent Details "+ str(e) +" attempted by "+str(request.user.username))
        json_data["status"] = 'Error'
    return HttpResponse(json.dumps(json_data))


def student_detail(request, slug):
    cur = connection.cursor()
    json_data = {}
    try:
        if request.method == 'GET':
            try:
                cur.execute("""select * from student_details where id = %s""",(int(slug), ))
                data_details = dictfetchall(cur)
                json_data["data"] = data_details
                json_data["status"] = status_keys.SUCCESS_STATUS
                logger_obj.info("Fetch Student Details  attempted by "+str(request.user.username))
            except Exception as e:
                print "---",e
                logger_obj.info("Fetch Student Details "+ str(e) +" attempted by "+str(request.user.username))
                json_data["status"] = status_keys.ERROR
        elif request.method == 'DELETE':
            try:
                cur.execute("""Update student_details set is_active = False 
                where id = %s""",(int(slug)))
                logger_obj.info("Delete Student Details  attempted by "+str(request.user.username))
                json_data["status"] = status_keys.REMOVE_STATUS
            except Exception as e:
                print "---",e
                logger_obj.info("Delete Student Details "+ str(e) +" attempted by "+str(request.user.username))
                json_data["status"] = status_keys.ERROR
        elif request.method == 'PUT':
            try:
#                 cur.execute("""Update tbl_dictator_master set dictator_name = %s, line_count = %s, tat_duration=%s, 
#                  created_by_id = %s, modified_by_id = %s, template_id = %s where dictator_id = %s""",
#                 (str(data['dictator_name']), float(data['line_count']), str(data['tat_duration']), 
#                 int(request.user.id), int(request.user.id), int('1') , int(slug)))
                logger_obj.info("Update Student Details  attempted by "+str(request.user.username))
                json_data["status"] = status_keys.UPDATE_STATUS
            except Exception as e:
                print "-------",e
                logger_obj.info("Update Student Details "+ str(e) +" attempted by "+str(request.user.username))
                json_data["status"] = status_keys.ERROR
    except Exception as e:
        print "---",e
        logger_obj.info("Get Student Details "+ str(e) +" attempted by "+str(request.user.username))
        json_data["status"] = status_keys.ERR0012
    return HttpResponse(json.dumps(json_data))
           
        


def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict."
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()]
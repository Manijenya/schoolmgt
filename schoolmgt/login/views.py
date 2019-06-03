# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging, json, string
import logging.handlers
from django.shortcuts import render,redirect,reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login,logout as django_logout
from django.conf import settings
from django.db import connection

logger_obj = logging.getLogger('logit')


# Login page view written here
class LoginView(View):
    ''' 
    02-Jun-2019 To login page loaded. And also check the user authentication
    @param request: Request Object
    @type request : Object
    @return:   HttpResponse or Redirect the another URL
    @author: MKM
    '''
    template_name = "login/login.html"
     
    def get(self, request, *args, **kwargs):
        # if request.user.is_authenticated():
        if request.user.is_authenticated:
            return HttpResponseRedirect('/School/')
        else:
            return render(request, self.template_name)
    
    def post(self, request, *args, **kwargs):
        tempt_dict = {}
        cur = connection.cursor()
        if 'uid' in request.session:
            tempt_dict[settings.STATUS_KEY] = settings.SUCCESS_STATUS
        else:
            try:
                data = request.POST.get('datas')
                if data:
                    #For Web Application API
                    datas = json.loads(data)
                    username = datas['username']
                    password = datas['password']
                    user = authenticate(username=username, password=password)  #authenticate function
                    if user:
                        login(request, user)
#                         cur.execute("""select rm.role_id, rm.role_name, au.username 
#                         from tbl_role_master rm inner join auth_user au on au.role_id = rm.role_id where au.id = %s """,
#                         (str(user.id),)) 
#                         role_datas= query.dictfetchall(cur)
#                         if len(role_datas) != 0:
#                             request.session["role_name"] = role_datas[0]['role_name']
#                             tempt_dict['role_name'] = role_datas[0]['role_name']
#                             tempt_dict['username'] = role_datas[0]['username']
                        tempt_dict[settings.STATUS_KEY] = settings.SUCCESS_STATUS
                    else:
                        tempt_dict[settings.STATUS_KEY] = settings.ERROR
                return HttpResponse(json.dumps(tempt_dict))
            except Exception as e:
                logger_obj.info("Login miss match "+str(e))
                tempt_dict[settings.STATUS_KEY] = settings.ERROR
                return HttpResponse(json.dumps(tempt_dict))
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginView, self).dispatch(request, *args, **kwargs)
    
def logout(request):
    '''
    logout process
    @param request: Request Object
    @type request : Object
    @return:   HttpResponse. This response redirect the URL to login page
    @author: MKM
    '''
    django_logout(request)
    request.session.clear()
    request.session.flush()
    return HttpResponseRedirect("/")

"""
Login View   and Logout URLS
"""
from django.conf.urls import url
from . import views
from .views import LoginView, logout

urlpatterns = [
    url(r'^$', LoginView.as_view(), name="login_page"),
    url(r'^logout/', logout, name="logout"),
   
]

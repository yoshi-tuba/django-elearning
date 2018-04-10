"""elearning URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import re_path
from courses.views import (course_detail, course_list, course_add, do_section, do_test, show_results)
from students.views import student_detail

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^course_detail/(?P<course_id>\d+)/$', course_detail, name='course_detail'),
    re_path(r'^student_detail/(?P<student_id>\d+)/$', student_detail, name='student_detail'),
    re_path(r'^course_add/$', course_add, name='course_add'),
    re_path(r'^section/(?P<section_id>\d+)/$', do_section, name='do_section'),
    re_path(r'^section/(?P<section_id>\d+)/test/$', do_test, name='do_test'),
    re_path(r'^section/(?P<section_id>\d+)/results/$', show_results, name='show_results'),
    re_path(r'^$', course_list),
]

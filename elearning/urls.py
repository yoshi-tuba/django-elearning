
from django.contrib import admin, auth
from django.urls import path  # previously called url
from django.urls import re_path, include


# testing for django.contrib.auth.urls namespace problem workaround
import auth_django.urls as auth_urls

# this thing is only imported at runtime?
from students.views import student_detail
from courses.views import (course_detail,
                           course_list,
                           course_add,
                           do_section,
                           do_test,
                           show_results)

urlpatterns = [
    path('admin/', admin.site.urls),

    # this just imports the list of urlpatterns inside django's contrib.auth.urls file
    path('', include(auth_urls, namespace='auth_django')),

    #re_path(r'^course_detail/(?P<course_id>\d+)/$', course_detail, name='course_detail'),
    # a class based view has their own naming conventions
    re_path(r'^course_detail/(?P<pk>\d+)/$', course_detail, name='course_detail'),
    path('student_detail/', student_detail, name='student_detail'),
    re_path(r'^section/(?P<section_id>\d+)/$', do_section, name='do_section'),
    re_path(r'^section/(?P<section_id>\d+)/test/$', do_test, name='do_test'),
    re_path(r'^section/(?P<section_id>\d+)/results/$', show_results, name='show_results'),

    path('course_add/', course_add, name='course_add'),
    re_path(r'^course_list/', course_list),

    path('', course_list),
]
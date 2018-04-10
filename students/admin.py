from django.contrib import admin

# this import allows us to build a user class with more security features
# if users were made before this was done, then we gotta change the password again, using
# 'manage.py changepassword username' and key it in in CLI
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from students.models import User##, Section, Question


# makes an admin for the app by inheriting from django's default model admin
class UserAdmin(BaseUserAdmin):
    pass
admin.site.register(User, UserAdmin)

# class SectionAdmin(admin.ModelAdmin):
#     pass
#
# admin.site.register(Section, SectionAdmin)
#
# class QuestionAdmin( admin.ModelAdmin):
#     pass
# admin.site.register(Question, QuestionAdmin)

# then register the database to lock it from random changes, using CourseAdmin as the administrator of this model (db)

from django.contrib import admin

# Register your models here.

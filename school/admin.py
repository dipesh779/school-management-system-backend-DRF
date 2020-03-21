from django.contrib import admin
from .models import School, Teacher, Staff, Subject, Student, Level

admin.site.register([School, Teacher, Subject, Student, Staff, Level])

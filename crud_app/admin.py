from django.contrib import admin
from .models import Student

class StudentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'age', 'gender']


admin.site.register(Student, StudentAdmin)


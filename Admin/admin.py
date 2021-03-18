from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import *

# Register your models here.
admin.site.register(custom_admin)
admin.site.register(student_type)
admin.site.register(course)
admin.site.register(departments)


@admin.register(students)
class studentTypeAdmin(ImportExportModelAdmin):
    list_display = ('Rollno','Name','Batch','Department')
    
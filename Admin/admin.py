from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import *

# Register your models here.
admin.site.register(admin_detail)
admin.site.register(student_type)
admin.site.register(course)

@admin.register(student_detail)
class studentTypeAdmin(ImportExportModelAdmin):
    list_display = ('Rollno','Name','Type','Batch','Department')
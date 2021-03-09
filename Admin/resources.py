from import_export import resources
from .models import student_detail

class StudentDetailResource(resources.ModelResource):
    class meta:
        model = student_detail
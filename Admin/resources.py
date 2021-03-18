from import_export import resources
from .models import student_detail
from .models import students

class StudentDetailResource(resources.ModelResource):
    class meta:
        model = students
from rest_framework.decorators import api_view, permission_classes
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .serializers import *
from .models import *
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist




@api_view(["GET","POST"])
# @csrf_exempt
# @permission_classes([IsAuthenticated])

def Authenticate(request):
    #method to authenticate users
    if request.method == "POST":
       try:
          admin_data = admin_detail.objects.get(username=request.data['username'],password=request.data['password'])
          return JsonResponse({'message':'Authentication Success'},safe=False,status=status.HTTP_200_OK)
       except ObjectDoesNotExist as e:
          return JsonResponse({'message':"Invalid username or password"},safe=False,status=status.HTTP_404_NOT_FOUND)
       except Exception:
          return JsonResponse({'message': 'Something  went wrong'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    #display admin details only for testing purpose removed in future
    if request.method == "GET":
        admins = admin_detail.objects.all()
        serializer = AdminSerializer(admins, many=True)
        return JsonResponse({'admins': serializer.data}, safe=False, status=status.HTTP_200_OK)
# Manage student detail 
@api_view(["GET","POST","DELETE","PUT"])

def Manage_student(request):
   if request.method == "POST":
      try:
         student = student_detail.objects.create(
            Rollno=request.data['Rollno'],
            Name=request.data['Name'],
            Type=request.data['Type'],
            Batch=request.data['Batch']
         )
         serializer = StudentSerializer(student)
         return JsonResponse({'Message':'Data added successfully','data':serializer.data},safe=False, status=status.HTTP_201_CREATED)
      except ObjectDoesNotExist as e:
         return JsonResponse({'Message':str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
      except Exception:
          return JsonResponse({'message': 'Something  went wrong'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
   
   #display student details
   if request.method == "GET":
        student = student_detail.objects.all()
        serializer = StudentSerializer(student, many=True)
        return JsonResponse({'students': serializer.data}, safe=False, status=status.HTTP_200_OK)
  
   # to delete an record in student detail 
   if request.method == "DELETE":
      try:
         student = student_detail.objects.get(id= request.data['id'])
         student.delete()
         return JsonResponse({'Message':'Deleted successfully'},safe=False, status=status.HTTP_204_NO_CONTENT) 
      except ObjectDoesNotExist as e:
         return JsonResponse({'Message':str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
      except Exception:
          return JsonResponse({'message': 'Something  went wrong'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
   # to edit an record in student detail by rollno
   if request.method == "PUT":
      try:
         student = student_detail.objects.get(Rollno=request.data['Rollno'])    
         serializer = StudentSerializer(instance=student, data=request.data)
         if serializer.is_valid():
            print('print')
            serializer.save()
         return JsonResponse({'updated_data':serializer.data}, safe=False, status=status.HTTP_201_CREATED)
      except ObjectDoesNotExist as e:
         return JsonResponse({'Message':str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
      except Exception:
          return JsonResponse({'message': 'Something  went wrong'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

   

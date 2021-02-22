from rest_framework.decorators import api_view, permission_classes
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .serializers import AdminSerializer
from .models import admin_detail
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
          return JsonResponse({'message':"Wrong username or password"},safe=False,status=status.HTTP_404_NOT_FOUND)
       except Exception:
          return JsonResponse({'message': 'Something  went wrong'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    #display admin details only for testing purpose removed in future
    if request.method == "GET":
        admins = admin_detail.objects.all()
        serializer = AdminSerializer(admins, many=True)
        return JsonResponse({'admins': serializer.data}, safe=False, status=status.HTTP_200_OK)

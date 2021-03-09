from django.shortcuts import render,redirect
from .forms import *
from .models import *
from .resources import StudentDetailResource
from django.contrib import messages
from tablib import Dataset
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError


def login(request):
   if request.method == 'GET':
      return render(request,'login.html')
   
   if request.method == 'POST':
      username = request.POST['user_name']
      return render(request,'home.html',{'username':username})

def add_student(request):
   types = student_type.objects.all()
   res = []
   for t in types:
      res.append(t.Name)

   if request.method == 'GET':
      return render(request,'add_student.html',{'types':res})


   if request.method == 'POST':
      student_detail_resource = StudentDetailResource()
      dataset = Dataset()
      students = request.FILES['stdFile']

      if not students.name.endswith('xlsx'):
         messages.info(request,"wrong file format")
         return render(request,'add_student.html',{'types':res})

      imported_data = dataset.load(students.read(),format='xlsx')
      for data in imported_data:
         value = student_detail(
            Rollno=data[0],
            Name=data[1],
            Department=data[2],
            Type=request.POST['type'],
            Batch=request.POST['batch'])
         value.save()
         messages.success(request,'Successfully updated')
      return render(request,'add_student.html',{'types':res})

def edit_student(request):
   types = student_type.objects.all()
   res = []
   for t in types:
      res.append(t.Name)
   if request.method == "GET":
      return render(request,'edit_student.html',{'types':res})
   
   if request.method == "POST":
      try:
        student = student_detail.objects.get(Rollno=request.POST['search'])
        return render(request,'edit_student.html',{'student':student,'types':res})
      except ObjectDoesNotExist:
        messages.info(request,'Data unavailable')
        return render(request,'edit_student.html',{'types':types})
   
   

def updateStudent(request):
   types = student_type.objects.all()
   res = []
   for t in types:
      res.append(t.Name)
      
   if request.method == "POST":
      student_detail.objects.filter(id=request.POST['id']).update(
         Name = request.POST['Name'],
         Type = request.POST['Type'],
         Department = request.POST['Department'],
         Batch = request.POST['Batch'],
         Rollno = request.POST['Rollno']
         )
      student = student_detail.objects.get(Rollno = request.POST['Rollno'])
      messages.success(request,'Successfully updated')
      return render(request,'edit_student.html',{'student':student,'types':res})

def deleteStudent(request,id):
   types = student_type.objects.all()
   res = []
   for t in types:
      res.append(t.Name)
   try:
      student = student_detail.objects.get(id=id)
      student.delete()
      messages.info(request,'Deleted successfully!')
      return render(request,'edit_student.html',{'student':student,'types':res})

   except ObjectDoesNotExist:
      messages.info(request,'Data unavailable')
      return render(request,'edit_student.html',{'types':types})

# Course section

def Course(request):
   if request.method == 'GET':
      types = student_type.objects.all()
      res = []
      for t in types:
          res.append(t.Name)
      batches = student_detail.objects.all()
      res1 = set()
      for i in batches:
         res1.add(i.Batch)
      courses = course.objects.all()
      return render(request,'course.html',{'courses':courses,'types':res,'batches':res1})

   if request.method == 'POST':
      try:
         data = course(
         courseBatch = request.POST['courseBatch'],
         studentType = request.POST['studentType'],
         courseType = request.POST['courseType'],
         courseCode= request.POST['courseCode'],
         courseTitle=request.POST['courseTitle'],
         courseDescription=request.POST['courseDescription']
         )
         data.save()
         messages.success(request,'Successfully updated')
      except IntegrityError:
         messages.success(request,'Cource with same code already exists')
      
      return redirect('/course/')

def editCourse(request,id):
   types = student_type.objects.all()
   res = []
   for t in types:
      res.append(t.Name)
   batches = student_detail.objects.all()
   res1 = set()
   for i in batches:
      res1.add(i.Batch)
   print(res)

   if request.method == 'GET':
      try:
         data = course.objects.get(id=id)
         return render(request,'edit_course.html',{'course':data,'types':res,'batches':res1,'cTypes':['NME','LS','PART-1']})
      except ObjectDoesNotExist:
         messages.info(request,'Data unavailable')
         return redirect('/course/')
   
   if request.method == 'POST':
      course.objects.filter(id=request.POST['id']).update(
         courseBatch = request.POST['courseBatch'],
         studentType = request.POST['studentType'],
         courseType = request.POST['courseType'],
         courseCode= request.POST['courseCode'],
         courseTitle=request.POST['courseTitle'],
         courseDescription=request.POST['courseDescription']
      )
      messages.success(request,'Successfully updated')
      return redirect('/course/')

def deleteCourse(request,id):
   try:
      data = course.objects.get(id=id)
      data.delete()
      messages.info(request,'Deleted successfully!')
      return redirect('/course/')

   except ObjectDoesNotExist:
      messages.info(request,'Data unavailable')
      return redirect('/course/')

def searchCourse(request):
   types = student_type.objects.all()
   res = []
   for t in types:
      res.append(t.Name)
  
   try:
      data = course.objects.get(courseCode=request.POST['search'])
      return render(request,'course.html',{'course':data,'types':res})
   except ObjectDoesNotExist:
      messages.info(request,'No records found')
      return render('/course/')

#seats allocation to the course

def seatAllocate(request):

   if request.method == 'GET':
      data = course.objects.all()
      return render(request,'allocate_seats.html',{'courses':data})

   if request.method == 'POST':
      try:
         course.objects.filter(id = request.POST['courseCode']).update(
             seats = request.POST['seats']
         )
         messages.success(request,'Successfully updated')
      except Exception as e:
         messages.info(request,"Something went wrong")
      return redirect("/addSeats/")

def editSeat(request,id):

   if request.method == 'GET':
      try:
         data = course.objects.get(id=id)
         return render(request,'edit_seat.html',{'course':data})
      except ObjectDoesNotExist:
         messages.info(request,'Data unavailable')
         return redirect('/addSeats/')

   if request.method == 'POST':
      try:
        course.objects.filter(id=request.POST['id']).update(
           courseCode= request.POST['courseCode'],
           seats = request.POST['seats']
         )
        messages.success(request,'Successfully updated')
      except ObjectDoesNotExist:
        messages.success(request,'Invalid request')
      return redirect('/addSeats/')

def deleteSeat(request,id):
   try:
      data = course.objects.get(id=id)
      data.delete()
      messages.info(request,'Deleted successfully!')
      return redirect('/addSeats/')

   except ObjectDoesNotExist:
      messages.info(request,'Data unavailable')
      return redirect('/addSeats/')

def searchSeat(request):
   try:
      data = course.objects.all()
      seats = course.objects.get(courseCode=request.POST['search'])
      return render(request,'allocate_seats.html',{'courses':data,'course':seats})
   except ObjectDoesNotExist:
      messages.info(request,'No records found')
      return render('/addSeats/')

#Reports
def liveReport(request):
   try:
      data = course.objects.all()
      print(data)
      return render(request,'live_report.html',{"data":data})
   except:
      messages.info(request,"Something went wrong")
      return render(request,'live_report.html')

def liveReportInd(request,id):
   try:
      courseData = course.objects.get(id=id)
      students = None
      return render(request,'live_report_inidvidual',{'data':students,'course':courseData})
   except Exception as e:
      messages.info(request,"Something went wrong")
      return redirect("/live-report/")
   
#site settings
def siteSet(request):
   
   if request.method == 'GET':
      data = siteSettings.objects.get(id=1)
      return render(request,'site_settings.html',{'site':data})

   if request.method == 'POST':
      try:
         siteSettings.objects.filter(id=1).update(
            startDate = request.POST['startDate'],
            endDate = request.POST['endDate']
         )
         messages.info(request,"Updated successfully!")
      except Exception as e:
         print(str(e))
         messages.info(request,'Something went wrong')
      return redirect("/site-settings/") 

   






         





   



     




      


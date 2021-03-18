from django.shortcuts import render,redirect
from .forms import *
from .models import *
from .resources import StudentDetailResource
from django.contrib import messages
from tablib import Dataset
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from passlib.hash import pbkdf2_sha256
from django.conf import settings 
from django.core.mail import send_mail
import random
import datetime

#helper functions

def getDepartment(data):
   result = ""
   for i in data:
      if i not in ['1','2','3','4','5','6','7','8','9','0']:
         result+= i
   return result

def isAuthenticated(request):
   secret = request.session.get('info','no')
   if secret == 'no':
      return False
   else:
      return pbkdf2_sha256.verify("Secret123",secret)

#view functions

def login(request):
   if request.method == 'GET':
       if isAuthenticated(request):
          return redirect('/')
       else:
          return render(request,'login.html')
   
   if request.method == 'POST':
      username = request.POST['user_name']
      password = request.POST['password']

      try:
        cuser = custom_admin.objects.get(username=username)
        if(cuser.verify_pass(password)):
           request.session['username'] = username
           request.session['info'] = pbkdf2_sha256.encrypt("Secret123",rounds=12000,salt_size=32)
           messages.info(request,"Successfully logged in")
        else:
           messages.info(request,"Wrong Credentials")

      except ObjectDoesNotExist:
         messages.info(request,"Wrong Credentials")
         
      return redirect('/login/')

def logout(request):
   try:
      del request.session['username']
      del request.session['info']
   except:
      pass
   return redirect('/login/')

def home(request):
   if isAuthenticated(request):
      username = request.session.get('username',"")
      return render(request,'home.html',{'username':username})
   else:
      messages.info(request,"login first")
      return redirect('/login/')

def add_student(request):
   if not isAuthenticated(request):
      messages.info(request,"login first")
      return redirect('/login/')

   if request.method == 'GET':
      types = student_type.objects.all()
      res = []
      for t in types:
          res.append(t.Name)
      data = students.objects.all()
      username = request.session.get('username',"")
      return render(request,'add_student.html',{'username':username,'students':data,'types':res})


   if request.method == 'POST':
      stdType = student_type.objects.get(Name=request.POST['studentType'])
      student_detail_resource = StudentDetailResource()
      dataset = Dataset()
      studentss = request.FILES['stdFile']

      if not studentss.name.endswith('xlsx'):
         messages.info(request,"wrong file format")
         return redirect('/add_student/')

      imported_data = dataset.load(studentss.read(),format='xlsx')
      for data in imported_data:
         value1 = departments(
            Name = getDepartment(data[0]).upper(),
            std_type = stdType
         )
         value = students(
            Rollno=data[0],
            Name=data[1],
            std_type= stdType,
            Department=getDepartment(data[0]).upper(),
            Batch=request.POST['batch'])
         try:
            value1.save()
         except IntegrityError:
            print(value1.std_type.Name)
            pass 
         try:
            value.save()
         except IntegrityError:
            print(value1.std_type.Name)
            pass  
      messages.success(request,'Successfully updated')
      return redirect('/add_student/')

def edit_student(request,id):
   if not isAuthenticated(request):
      messages.info(request,"login first")
      return redirect('/login/')

   if request.method == "GET":
      types = student_type.objects.all()
      res = []
      for t in types:
          res.append(t.Name)
      username = request.session.get('username',"")
      try:
        data = students.objects.get(id=id)
      except ObjectDoesNotExist:
        pass
      return render(request,'edit_student.html',{'student':data,'username':username,'types':res})
   
   if request.method == "POST":
      try:
         stdType = student_type.objects.get(Name=request.POST['studentType']) 
         departments.objects.filter(Name=request.POST['Department']).update(
            std_type = stdType
         )
         students.objects.filter(id=request.POST['id']).update(
          Name = request.POST['Name'],
          Department = request.POST['Department'],
          std_type = stdType,
          Batch = request.POST['Batch'],
          Rollno = request.POST['Rollno']
          )
         messages.info(request,'Successfully updated!')
      except ObjectDoesNotExist:
         messages.info(request,'Data unavailable')
      return redirect('/add_student/')
   

def deleteStudent(request,id):
   if not isAuthenticated(request):
      messages.info(request,"login first")
      return redirect('/login/')
   try:
      student = students.objects.get(id=id)
      student.delete()
      messages.info(request,'Deleted successfully!')
   except ObjectDoesNotExist:
      messages.info(request,'Data unavailable')
   return redirect('/add_student/')
   

# Course section
def Course(request):
   if not isAuthenticated(request):
      messages.info(request,"login first")
      return redirect('/login/')

   if request.method == 'GET':
      types = student_type.objects.all()
      res = []
      for t in types:
          res.append(t.Name)
      batches = students.objects.all()
      res1 = set()
      for i in batches:
         res1.add(i.Batch)
      courses = course.objects.all()
      Cdict = []
      for c in courses:
         Cdict.append({
            'id':c.id,
            'courseBatch':c.courseBatch,
            'courseType':c.courseType,
            'courseCode':c.courseCode,
            'courseTitle':c.courseTitle,
            'stdType': (c.getStdTypes()).split(","),
            'cdeps':(c.getDeps()).split(",")
         })
     
      username = request.session.get('username',"")
      return render(request,'course.html',{'username':username,'courses':Cdict,'types':res,'batches':res1})

   if request.method == 'POST':
      try:
         data = course(
             courseBatch=request.POST['courseBatch'],
             courseType=request.POST['courseType'],
             courseCode=request.POST['courseCode'],
             courseTitle=request.POST['courseTitle'],
         )
         data.save()
         messages.success(request,'Successfully updated')
      except IntegrityError:
         messages.success(request,'Cource with same code already exists')
      
      return redirect('/course/')

def addType(request,id):
   if not isAuthenticated(request):
      messages.info(request,"login first")
      return redirect('/login/')

   if request.method == 'GET':
      try:
         data = course.objects.get(id=id)
      except ObjectDoesNotExist:
         messages.info(request,"Data not found")
         return redirect('/course/') 
      types = student_type.objects.all()
      res = []
      for t in types:
         res.append(t.Name)
      username = request.session.get('username',"")
      selected_types = data.std_types.all()
      return render(request,'addType.html',{'username':username,'course':data,'types':res,'stypes':selected_types})

   if request.method == 'POST':
      try:
         typed = student_type.objects.get(Name=request.POST['student_type'])
      except ObjectDoesNotExist:
         messages.info(request,"Data not found")
         return redirect('/course/')
      try:
         coursed = course.objects.get(id=id)
      except ObjectDoesNotExist:
         messages.info(request,"Data not found")
         return redirect('/course/')
      coursed.std_types.add(typed)
      messages.info(request,"successfully updated!")
      return redirect("/addType/"+str(id))

def remType(request,id,id1):
   if not isAuthenticated(request):
      messages.info(request,"login first")
      return redirect('/login/')

   try:
      data = course.objects.get(id=id)
      data1 = student_type.objects.get(id=id1)
      data.std_types.remove(data1)
   except ObjectDoesNotExist:
      messages.info(request,"Removed successfully!")
   return redirect('/addType/'+str(id))

def addDept(request,id):
   if not isAuthenticated(request):
      messages.info(request,"login first")
      return redirect('/login/')
   if request.method == 'GET':
      try:
         depData = []
         data = course.objects.get(id=id)
         data1 = data.std_types.all()
         data2 = set()
         for i in data1:
            temp = departments.objects.filter(std_type=i)
            for j in temp:
               data2.add(j.Name)
         data3 = data.deps.all()
         data4 = []
         for i in data3:
            data4.append(i.Name)
         
         username = request.session.get('username',"")
         return render(request, 'addDept.html',{'username':username,'dept':data2,'types':data1,'course':data,'sdeps':data4,'sdeps2':data3}) 
      except ObjectDoesNotExist:
         messages.info(request, "Something went wrong")
         return redirect("/course/")
   
   if request.method == 'POST':
      try:
         dept = departments.objects.get(Name=request.POST['dept'])
         cs = course.objects.get(id=id)
         cs.deps.add(dept)
         messages.info(request,"successfully updated!")
         return redirect("/addDept/"+str(id))

      except ObjectDoesNotExist:
         messages.info(request,"Something went wrong")
         return redirect("/course/")
      

def remDeps(request,id,id1):
   if not isAuthenticated(request):
      messages.info(request,"login first")
      return redirect('/login/')

   try:
      data = course.objects.get(id=id)
      data1 = departments.objects.get(id=id1)
      data.deps.remove(data1)
   except ObjectDoesNotExist:
      messages.info(request,"Removed successfully!")
   return redirect('/addDept/'+str(id))

      

def editCourse(request,id):
   if not isAuthenticated(request):
      messages.info(request,"login first")
      return redirect('/login/')

   types = student_type.objects.all()
   res = []
   for t in types:
      res.append(t.Name)
   batches = student_detail.objects.all()
   res1 = set()
   for i in batches:
      res1.add(i.Batch)

   if request.method == 'GET':
      try:
         data = course.objects.get(id=id)
         username = request.session.get('username',"")
         return render(request,'edit_course.html',{'course':data,'types':res,'batches':res1,'cTypes':['NME','LS','PART-1']})
      except ObjectDoesNotExist:
         messages.info(request,'Data unavailable')
         return redirect('/course/')
   
   if request.method == 'POST':
      try:
         course.objects.filter(id=request.POST['id']).update(
            courseBatch=request.POST['courseBatch'],
            courseType=request.POST['courseType'],
            courseCode=request.POST['courseCode'],
            courseTitle=request.POST['courseTitle'],
         )
         messages.success(request, 'Successfully updated')
      except ObjectDoesNotExist:
         messages.info(request, 'Data unavailable')
      return redirect('/course/')

def deleteCourse(request,id):
   if not isAuthenticated(request):
      messages.info(request,"login first")
      return redirect('/login/')

   try:
      data = course.objects.get(id=id)
      data.delete()
      messages.info(request,'Deleted successfully!')
      return redirect('/course/')

   except ObjectDoesNotExist:
      messages.info(request,'Data unavailable')
      return redirect('/course/')

#adding additional details to the course
def coursead(request):
   if not isAuthenticated(request):
      messages.info(request,"login first")
      return redirect('/login/')

   if request.method == 'GET':
      try:
         data = course.objects.all()
         data1 = cdetails.objects.all()
         data2 = []
         for i in data1:
            data2.append(i.cs.courseCode)
         username = request.session.get('username',"")
         return render(request,'coursead.html',{'course':data,'courseW':data1,'courseS':data2})
      except Exception as e:
         messages.info(request,"Something went wrong")
         return redirect('/course/')

   if request.method == 'POST':
      cimg = request.FILES['cimg']
      if not ((cimg.name.endswith('jpg') or cimg.name.endswith('JPG')) or (cimg.name.endswith('PNG') or cimg.name.endswith('png'))):
         messages.info(request,"wrong file format")
         return redirect('/coursead/')

      try:
         c = course.objects.get(id=request.POST['cid'])
         data = cdetails(
            cs=c,
            description=request.POST['cd'],
            img = cimg
         )
         data.save()
         messages.info(request,"updated successfully")
      except Exception as e:
         print(str(e))
         messages.info(request,"Something went wrong")
      return redirect("/coursead/")

def editCoursead(request, id):
   if not isAuthenticated(request):
      messages.info(request,"login first")
      return redirect('/login/')
   
   if request.method == 'GET':
      data = cdetails.objects.get(id=id)
      username = request.session.get('username',"")
      return render(request,'editcoursead.html',{'course':data})

   if request.method == 'POST':
      try:
        if len(request.FILES)>0:
           data = cdetails.objects.get(id=id)
           c = data.cs
           newData = cdetails(
              cs = c,
              description=request.POST['des'],
              img = request.FILES['img']
           )
           newData.save()
           nid = newData.id
           data.delete()
           messages.info(request,"Updated successfully")
           return redirect('/editCoursead/'+str(nid))
        else:
           print("hellog")
           cdetails.objects.filter(id=id).update(description=request.POST['des'])
           messages.info(request,"Updated successfully")
           return redirect('/editCoursead/'+str(id))
      except Exception as e:
         print(str(e))
         messages.info(request,"Something went wrong")
         return redirect('/editCoursead/'+str(id))


def deleteCoursead(request, id):
   if not isAuthenticated(request):
      messages.info(request,"login first")
      return redirect('/login/')

   try:
      data = cdetails.objects.get(id=id)
      data.delete()
      messages.info(request,"Deleted successfully")
   except Exception as e:
      print(str(e))
      messages.info(request,"Something went wrong")
   return redirect("/coursead/")
   

#seats allocation to the course

def seatAllocate(request):
   if not isAuthenticated(request):
      messages.info(request,"login first")
      return redirect('/login/')

   if request.method == 'GET':
      data = course.objects.all()
      username = request.session.get('username',"")
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
   if not isAuthenticated(request):
      messages.info(request,"login first")
      return redirect('/login/')

   if request.method == 'GET':
      try:
         data = course.objects.get(id=id)
         username = request.session.get('username',"")
         return render(request,'edit_seat.html',{'course':data})
      except ObjectDoesNotExist:
         messages.info(request,'Data unavailable')
         return redirect('/addSeats/')

   if request.method == 'POST':
      try:
        course.objects.filter(id=request.POST['id']).update(
           seats = request.POST['seats']
         )
        messages.success(request,'Successfully updated')
      except ObjectDoesNotExist:
        messages.success(request,'Invalid request')
      return redirect('/addSeats/')

def deleteSeat(request,id):
   if not isAuthenticated(request):
      messages.info(request,"login first")
      return redirect('/login/')
   try:
      course.objects.filter(id=id).update(
           seats = 0
      )
      messages.info(request,'Deleted successfully!')
      return redirect('/addSeats/')

   except ObjectDoesNotExist:
      messages.info(request,'Data unavailable')
      return redirect('/addSeats/')

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
   if not isAuthenticated(request):
      messages.info(request,"login first")
      return redirect('/login/')
   
   if request.method == 'GET':
      # data = siteSettings.objects.get(id=1)
      data = siteSettings.objects.get(id=1)
      return render(request,'site_settings.html',{'site':data})

   if request.method == 'POST':
      try:
         # siteSettings.objects.filter(id=1).update(
         #    startDate = request.POST['startDate'],
         #    endDate = request.POST['endDate']
         # )
         site = siteSettings(
            startDate = request.POST['startDate'],
            endDate = request.POST['endDate']
         )
         site.save()
         messages.info(request,"Updated successfully!")
      except Exception as e:
         print(str(e))
         messages.info(request,'Something went wrong')
      return redirect("/site-settings/") 

# functions handling forget password section
def forgetPass(request):

   if request.method == 'GET':
      try:
         data = custom_admin.objects.get(id=1)
         return render(request,'forgetpass.html',{"admin":data.email})
      except ObjectDoesNotExist:
         messages.info(request,"something went wrong")
         return redirect('/')

   if request.method == 'POST':
      try:
         data = custom_admin.objects.get(id=1)
         otp = random.randint(12512,45267)
         data.otp = otp
         now = datetime.datetime.now()
         now_plus_10 = now + datetime.timedelta(minutes = 10)
         data.otpExpires = now_plus_10
         data.save()
         subject = 'Password recovery'
         message = f'{otp}, is the otp for changing password'
         email_from = settings.EMAIL_HOST_USER 
         recipient_list = [data.email, ] 
         send_mail( subject, message, email_from, recipient_list ) 
         messages.info(request,"OTP sent")
      except Exception as e:
         print(str(e))
         messages.info(request,"Something went wrong")
      return redirect('/verifyOtp/')

def verifyOtp(request):
   if request.method == 'GET':
      return render(request,'verifyOtp.html')

   if request.method == 'POST':
      try:
         data = custom_admin.objects.get(id=1)
         now = datetime.datetime.now()
         otp_expires = data.otpExpires
         diff1 = int(otp_expires.hour)-int(now.hour)
         diff = int(otp_expires.minute)-int(now.minute)
         if diff1>0:
            diff += 60
         if diff > 0 and data.otp == request.POST['otp']:
            messages.info(request,"Otp verified")
            data.otpExpires = None
            request.session['info2'] = pbkdf2_sha256.encrypt(data.otp,rounds=12000,salt_size=32)
            return redirect('/changePass/')
         else:
            if data.otp != request.POST['otp']:
               messages.info(request,"Wrong otp")
            else:
               messages.info(request,"Otp expired try again")
            return redirect("/")
      except ObjectDoesNotExist:
         messages.info(request,"Something went wrong")

def changePass(request):
   try:
      temp = request.session.get("info2","")
      data = custom_admin.objects.get(id=1)
      if pbkdf2_sha256.verify(data.otp,temp):
         pass
      else:
         messages.info(request,"Not allowed")
         return redirect("/")
   except Exception as e:
      print(str(e))
      messages.info(request,"something went wrong")
      return redirect("/")
      

   if request.method == "GET":
      username = request.session.get('username',"")
      return render(request,"changePass.html",{'username':username})

   if request.method == "POST":
      try:
         data = custom_admin.objects.get(id=1)
         if request.POST['pass'] == request.POST['RePass']:
            data.otp = None
            del request.session['info2']
            data.save()
            messages.info(request,"password changed successfully")
            return redirect('/login/')
         else:
            messages.info(request,"New password & Re-enter password should be same")
            return redirect('/changePass/')
        
      except Exception as e:
         print("exception",str(e))
         messages.info(request,"something went wrong")
         return redirect("/")

#module for changing password when user logged in
def changePass1(request):
   if not isAuthenticated(request):
      messages.info(request,"login first")
      return redirect('/login/')
      
   if request.method == "GET":
      username = request.session.get('username',"")
      return render(request,"changePass.html",{'username':username,'isLogged':"yes"})

   if request.method == "POST":
      try:
         data = custom_admin.objects.get(id=1)
         if data.verify_pass(request.POST['oldPass']):
            if request.POST['pass'] == request.POST['RePass']:
               data.password = pbkdf2_sha256.encrypt(request.POST['pass'],rounds=12000,salt_size=32)
               data.save()
               messages.info(request,"Password changed")
               return redirect("/")
            else:
               messages.info(request,"New password & Re-enter password should be same")
               return redirect('/changePass1/')
         else:
             messages.info(request,"Enter correct old password")
             return redirect('/changePass1/')
      except Exception as e:
         print("Exception",str(e))
         messages.info(request,"something went wrong")
         return redirect("/")

   





   









   






         





   



     




      


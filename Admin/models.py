from django.db import models
from passlib.hash import pbkdf2_sha256
import base64

# Create your models here.
class custom_admin(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=300)
    role = models.CharField(max_length=15,default='Admin')
    email =models.EmailField(max_length=125,default='narmatha14amc@gmail.com')
    otp = models.CharField(max_length=10,default=None,blank=True, null=True)
    otpExpires = models.DateTimeField(default=None,blank=True, null=True)

    def __str__(self):
        return self.username

    def verify_pass(self,rpass):
        return pbkdf2_sha256.verify(rpass,self.password)

class student_type(models.Model):
    Name = models.CharField(max_length=50,unique = True)
    def __str__(self):
        return self.Name

class departments(models.Model):
    Name = models.CharField(max_length=10,unique=True)
    std_type = models.ForeignKey(student_type,on_delete=models.CASCADE)
    def __str__(self):
        return self.Name


class students(models.Model):
    Rollno = models.CharField(max_length=50,unique=True)
    Name = models.CharField(max_length=100)
    Batch = models.CharField(max_length=50)
    Department = models.CharField(max_length=10)
    std_type = models.ForeignKey(student_type,on_delete=models.CASCADE)
    def __str__(self):
        return self.Rollno

        
class student_detail(models.Model):
    Rollno = models.CharField(max_length=10,unique = True)
    Name = models.CharField(max_length=100)
    Type = models.CharField(max_length=50)
    Batch = models.CharField(max_length=50)
    Department = models.CharField(max_length=10)
    def __str__(self):
        return self.Name



#models for courses
class course(models.Model):
    courseBatch = models.CharField(max_length=50)
    std_types = models.ManyToManyField(student_type)
    deps = models.ManyToManyField(departments)
    courseType = models.CharField(max_length=50)
    courseCode = models.CharField(max_length=10,unique = True)
    courseTitle = models.CharField(max_length=10)
    seats = models.IntegerField(default=0)
    #string format 
    def __str__(self):
        return self.courseTitle


    #method for getting std_types
    def getStdTypes(self):
        res = ""
        for i in self.std_types.all():
            res +=i.Name+","
        return res

    def getDeps(self):
        res = ""
        for i in self.deps.all():
            res += i.Name+','
        return res


#additional detail for courses
class cdetails(models.Model):
    cs = models.ForeignKey(course,on_delete=models.CASCADE)
    description = models.TextField()
    img = models.ImageField(upload_to='images/') 

    def delete(self, using=None, keep_parents=False):
        self.img.storage.delete(self.img.name)
        super().delete()


#model for site activation and deactivation
class siteSettings(models.Model):
    startDate = models.DateField()
    endDate = models.DateField()
    
#model for forgetpassword


from django.db import models

# Create your models here.
class admin_detail(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=300)
    role = models.CharField(max_length=15)
    mobile = models.CharField(max_length=10)
    def __str__(self):
        return self.username
        
class student_detail(models.Model):
    Rollno = models.CharField(max_length=10,unique = True)
    Name = models.CharField(max_length=100)
    Type = models.CharField(max_length=50)
    Batch = models.CharField(max_length=50)
    Department = models.CharField(max_length=10)
    def __str__(self):
        return self.Name

class student_type(models.Model):
    Name = models.CharField(max_length=50,unique = True)
    def __str__(self):
        return self.Name


#models for courses
class course(models.Model):
    courseBatch = models.CharField(max_length=50)
    studentType = models.CharField(max_length=50)
    courseType = models.CharField(max_length=50)
    courseCode = models.CharField(max_length=10,unique = True)
    courseTitle = models.CharField(max_length=10)
    courseDescription = models.TextField()
    seats = models.IntegerField(default=0)
    seats_opted = models.IntegerField(default=0)
    seats_avail = models.IntegerField(default=0)
    # courserimage
    def __str__(self):
        return self.courseTitle


#model for site activation and deactivation
class siteSettings(models.Model):
    startDate = models.DateField()
    endDate = models.DateField()
    
#model for booking

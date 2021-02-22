from django.db import models

# Create your models here.
class admin_detail(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=300)
    role = models.CharField(max_length=15)
    mobile = models.CharField(max_length=10)

    def __str__(self):
        return self.username
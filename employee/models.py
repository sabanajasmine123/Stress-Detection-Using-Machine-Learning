from django.db import models
from manager.models import *

# Create your models here.
class employees(models.Model):
    name=models.CharField(max_length=20)
    email=models.CharField(max_length=50)
    phoneno=models.CharField(max_length=10)
    password=models.CharField(max_length=20)
    image=models.ImageField(upload_to='img')
    address=models.CharField(max_length=100)
    department=models.CharField(max_length=20)
    qualification=models.CharField(max_length=50)
    experience=models.CharField(max_length=20)
    managerid=models.ForeignKey(manager,on_delete=models.CASCADE)
    stress=models.BooleanField(default="False")
    message=models.BooleanField(default="False")
    confirm=models.BooleanField(default="False")
    reject=models.BooleanField(default="False")
    okay=models.BooleanField(default="False")
    sendmail=models.BooleanField(default="False")
    msg=models.CharField(max_length=200)



    def __str__(self) :
        return self.name
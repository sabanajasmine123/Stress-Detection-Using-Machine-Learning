from django.db import models

# Create your models here.
class manager(models.Model):
    name=models.CharField(max_length=20)
    email=models.CharField(max_length=50)
    phoneno=models.CharField(max_length=10)
    password=models.CharField(max_length=20)
    image=models.ImageField(upload_to='img')
    address=models.CharField(max_length=20)
    department=models.CharField(max_length=20)
    qualification=models.CharField(max_length=20)
    experience=models.CharField(max_length=20)

    def __str__(self) :
        return self.name
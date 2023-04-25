from django.shortcuts import render,redirect
from django.contrib import messages
from .models import *
from employee.models import *
import os
from stress.settings import EMAIL_HOST_USER
from . import forms
from django.core.mail import send_mail
import random
import string
from django.conf import settings

# Create your views here.
def mhome(request):
    return render(request,'manager/mindex.html')

def mlogin(request):
    if request.method=="POST":
        try:
            email=request.POST.get('email')
            password=request.POST.get('password')
            data=manager.objects.get(email=email,password=password)
            request.session['name']=data.name
            request.session['id']=data.id
            return redirect('mhome')
        except manager.DoesNotExist as e:
            messages.info(request,'Incorrect Password or Email')
    return render(request,'manager/mlogin.html')


def mregistration(request):
    if request.method=="POST":
        name=request.POST.get("name")
        email=request.POST.get("email")
        phoneno=request.POST.get("phoneno")
        address=request.POST.get("address")
        password=request.POST.get("password")
        cpassword=request.POST.get("cpassword")
        image=request.FILES.get("image")
        department=request.POST.get("department")
        qualification=request.POST.get("qualification")
        experience=request.POST.get("experience")
        if password==cpassword:
            if manager.objects.filter(email=email).exists():
                messages.info(request,'Email already exists')
            elif manager.objects.filter(phoneno=phoneno).exists():
                messages.info(request,'Phonenumber already exists')
            else:
                save_value=manager(name=name,email= email, phoneno=phoneno,address=address,
                            password= password,image=image,department=department,qualification=qualification,experience=experience)
                save_value.save()
                return redirect("mlogin")
        else:
             messages.info(request,'password not match')
    return render(request,'manager/mregistration.html')


def mprof(request):
    id=request.session['id']
    pro=manager.objects.get(id=id)
    return render(request,'manager/profile.html',{'pro':pro})


def meditprof(request,id):
    edit_pro=manager.objects.get(id=id)
    if request.method=="POST":
        if len(request.FILES)!=0:
            if len(edit_pro.image)>0:
                os.remove(edit_pro.image.path)
            edit_pro.image = request.FILES.get("image")
        edit_pro.name = request.POST.get("name")
        edit_pro.email = request.POST.get("email")
        edit_pro.phoneno=request.POST.get("phoneno")
        edit_pro.password=request.POST.get("password")
        edit_pro.department=request.POST.get("department")
        edit_pro.address=request.POST.get("address")
        edit_pro.qualification=request.POST.get("qualification")
        edit_pro.experience=request.POST.get("experience")
        edit_pro.save()
        return redirect('mhome')
    return render(request,"manager/meditprof.html",{"edit":edit_pro})


def addemployees(request):
    id=request.session['id']
    data=manager.objects.get(id=id)
    if request.method=="POST":
        name=request.POST.get("name")
        email=request.POST.get("email")
        phoneno=request.POST.get("phoneno")
        address=request.POST.get("address")
        image=request.FILES.get("image")
        department=request.POST.get("department")
        mid=id
        if employees.objects.filter(email=email).exists():
            messages.info(request,'Email already exists')
        elif employees.objects.filter(phoneno=phoneno).exists():
            messages.info(request,'Phonenumber already exists')
        else:
            save_value=employees(name=name,email=email,phoneno=phoneno,address=address,image=image,department=department,managerid_id=mid)
            save_value.save()
            return redirect("mhome")
    return render(request,'manager/addemployee.html',{'data':data})


def vemployee(request):
    id=request.session['id']
    pro=employees.objects.filter(managerid=id)
    uid=request.session['id']
    prof=manager.objects.filter(id=uid)
    return render(request,'manager/viewemployee.html',{'pro':pro,'prof':prof})


def sendemail(request,id):
    owner=employees.objects.get(id=id)
    sub = forms.Subscribe()
    # if request.method == 'POST':
    sub =owner.email
    name=owner.name
    subject = 'Hi, '+format(name) 
    recepient = str(sub)
      
    # get random password pf length 8 with letters, digits, and symbols
    characters = string.ascii_letters + string.digits 
    password = ''.join(random.choice(characters) for i in range(8))
    employees.objects.filter(id=id).update(password=password)
    employees.objects.filter(id=id).update(sendmail=True)
        
    message = '''Welcome to Office site.
    You can login with this password : ''' +format(password)
    send_mail(subject, message, EMAIL_HOST_USER, [recepient], fail_silently = False)
    return redirect('mhome')

def emessage(request,id):
    employees.objects.filter(id=id).update(stress=False)
    employees.objects.filter(id=id).update(message=True)
    emp=employees.objects.get(id=id)
    if request.method=="POST":
        emp.msg=request.POST.get("msg")
        emp.save()
        return redirect('mhome')
    return render(request,"manager/emessage.html")

def okay(request,id):
    employees.objects.filter(id=id).update(confirm=False)
    employees.objects.filter(id=id).update(reject=False)
    employees.objects.filter(id=id).update(okay=True)
    employees.objects.filter(id=id).update(message=False)
    return redirect('mhome')


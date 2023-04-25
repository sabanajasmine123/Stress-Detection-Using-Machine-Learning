from django.shortcuts import render,redirect
from django.contrib import messages
from .models import *
import os

from keras.models import load_model
from time import sleep
from keras.preprocessing.image import img_to_array
from keras.preprocessing import image
import cv2
import numpy as np
# Create your views here.

def ehome(request):
    id=request.session['id']
    pro=employees.objects.get(id=id)
    return render(request,'employee/eindex.html',{'pro':pro})

def elogin(request):
    if request.method=="POST":
        try:
            email=request.POST.get('email')
            password=request.POST.get('password')
            data=employees.objects.get(email=email,password=password)
            request.session['name']=data.name
            request.session['id']=data.id
            return redirect('estress')
        except manager.DoesNotExist as e:
            messages.info(request,'Incorrect Password or Email')
    return render(request,'employee/elogin.html')

def eprof(request):
    id=request.session['id']
    pro=employees.objects.get(id=id)
    return render(request,'employee/eprofile.html',{'pro':pro})


def eeditprof(request,id):
    edit_pro=employees.objects.get(id=id)
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
        return redirect('estress')
    return render(request,"employee/eeditprof.html",{"edit":edit_pro})


def estress(request):
    id=request.session['id']
    pro=employees.objects.get(id=id)
    if request.method == "POST":
        face_classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        classifier =load_model('model.h5')

        emotion_labels = ['Angry','Disgust','Fear','Happy','Neutral', 'Sad', 'Surprise']
        count=0
        cap = cv2.VideoCapture(0)

        while True:
            _, frame = cap.read()
            labels = []
            gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            faces = face_classifier.detectMultiScale(gray)

            for (x,y,w,h) in faces:
                if w>100:
                    cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,255),2)
                    roi_gray = gray[y:y+h,x:x+w]
                    roi_gray = cv2.resize(roi_gray,(48,48),interpolation=cv2.INTER_AREA)


                    if np.sum([roi_gray])!=0:
                        roi = roi_gray.astype('float')/255.0
                        roi = img_to_array(roi)
                        roi = np.expand_dims(roi,axis=0)

                        prediction = classifier.predict(roi)[0]
                        label=emotion_labels[prediction.argmax()]
                        label_position = (x,y)
                        if label == 'Angry':
                            label='Stressed' 
                            count += 1
                        elif label =='Sad':
                            label='Stressed'
                            count += 1
                        elif label =='Happy':
                            label='Normal'
                            count= 0
                        elif label =='Disgust':
                            label='Stressed'
                            count += 1
                        elif label == 'Fear':
                            label='Stressed'
                            count += 1
                        elif label == 'Surprise':
                            label='Normal'
                            count= 0
                        else:
                            label="Normal"

                        cv2.putText(frame,label + str(count/10*100),label_position,cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
                        if count>= 10: 
                            employees.objects.filter(id=id).update(stress=True) 
                            cv2.putText(frame,'Stressed !!!!',(30,80),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
                            break
                    else:
                        cv2.putText(frame,'No Faces',(30,80),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
                        count = 0
            cv2.imshow('Emotion Detector',frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
    return render(request,'employee/eindex.html',{'pro':pro})


def confirm(request):
    id=request.session['id']
    employees.objects.filter(id=id).update(confirm=True)
    employees.objects.filter(id=id).update(reject=False)
    return redirect('estress')



def reject(request):
    id=request.session['id']
    employees.objects.filter(id=id).update(confirm=False)
    employees.objects.filter(id=id).update(reject=True)
    return redirect('estress')
from django.urls import path 
from . import views


urlpatterns = [
    path('mhome',views.mhome,name='mhome'),
    path('mlogin',views.mlogin,name='mlogin'),
    path('mregistration',views.mregistration,name='mregistration'),
    path('mprof',views.mprof,name='mprof'),
    path('meditprof<int:id>',views.meditprof,name='meditprof'),
    path('addemployees',views.addemployees,name='addemployees'),
    path('vemployee',views.vemployee,name='vemployee'),
    path('sendemail<int:id>',views.sendemail,name='sendemail'),
]

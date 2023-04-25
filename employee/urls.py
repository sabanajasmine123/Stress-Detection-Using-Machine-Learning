from django.urls import path 
from . import views


urlpatterns = [
    path('ehome',views.ehome,name='ehome'),
    path('elogin',views.elogin,name='elogin'),
    path('eprof',views.eprof,name='eprof'),
    path('eeditprof<int:id>',views.eeditprof,name='eeditprof'),
    path('estress',views.estress,name='estress'),
    path('confirm',views.confirm,name='confirm'),
    path('reject',views.reject,name='reject'),

]

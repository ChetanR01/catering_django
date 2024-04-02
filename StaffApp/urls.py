from django.urls import path
from StaffApp.views import *

urlpatterns = [
    path('',Userorder,name='u-order'),
    path('confirm_order/',confirm_order,name='confirm_order'),
    path('ingredients/',ingredients,name='ingredients'),
    path('staff_login/',staffLogin,name="staff-login"),
]

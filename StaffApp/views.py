from django.shortcuts import render,redirect
from UserApp.models import *
from django.urls import reverse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.

@login_required(login_url='/staff/staff_login/')
def Userorder(request):
    data = Order.objects.all().prefetch_related(
        'items__dish__ingredients'
    )

    return render(request, 'u_orders.html', context={'data': data})

@login_required(login_url='/staff/staff_login/')
def ingredients(request):
    data = Ingredient.objects.all()
    return render(request, 'ingredients.html',context={'data':data})


def staffLogin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        print(user.role)
        if user is not None:
            if user.role == 'User':
                messages.add_message(request, messages.ERROR, "Invalid Email or Password")
                return redirect(reverse('staff-login'))
            else:
                login(request, user)
                return redirect(reverse('u-order'))
        else:
            messages.add_message(request, messages.ERROR, "Email or Password Invalid")
            return redirect(reverse('staff-login'))

    return render(request,'staff_login.html')

def confirm_order(request):

    id = request.GET['id']
    print("id=",id)
    order = Order.objects.get(id=id)
    order.status = "Confirmed"
    order.save()
    return redirect('/staff')

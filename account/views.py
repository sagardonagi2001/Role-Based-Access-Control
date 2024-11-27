from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import SignUpForm, LoginForm

# Create your views here.

def index(request):
    return render(request, 'index.html')
def register(request):
    msg = None
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            msg = 'user created'
            return redirect('login_view')
        else:
            msg = 'form is not valid'
    else:
        form = SignUpForm()
    return render(request,'register.html', {'form': form, 'msg': msg})


def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # Check if the user is an admin, customer, or employee
                if user.is_admin:
                    return redirect('adminpage')  # Admin can access all pages
                elif user.is_customer:
                    return redirect('customer')  # Redirect to customer page
                elif user.is_employee:
                    return redirect('employee')  # Redirect to employee page
                else:
                    msg = 'User role is undefined'
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating form'
    return render(request, 'login.html', {'form': form, 'msg': msg})

def admin(request):
    # Only allow admins to access this page
    if not request.user.is_authenticated or not request.user.is_admin:
        messages.error(request, "You do not have permission to view this page.")
        return redirect('login_view')  # Redirect to login page if not admin
    return render(request, 'admin.html')

def customer(request):
    # Only allow customers to access this page
    if not request.user.is_authenticated or not request.user.is_customer:
        messages.error(request, "You do not have permission to view this page.")
        return redirect('login_view')  # Redirect to login page if not customer
    return render(request, 'customer.html')

def employee(request):
    # Only allow employees to access this page
    if not request.user.is_authenticated or not request.user.is_employee:
        messages.error(request, "You do not have permission to view this page.")
        return redirect('login_view')  # Redirect to login page if not employee
    return render(request, 'employee.html')

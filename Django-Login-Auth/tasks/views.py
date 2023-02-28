from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TasksForm
from .models import Task



# Create your views here.

def home(request):
    return render(request, 'home.html')


def signup(request):
    
    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm
        })
        
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username=request.POST['username'], 
                password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('tasks')
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': 'User already exists'
                })
        return render(request, 'signup.html', {
            'form': UserCreationForm,
            'error': 'Password do not match'
        })


def tasks(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    
    return render(request, 'tasks.html', {'tasks': tasks})

def create_task(request):
    
    if request.method == 'GET':
        return render(request, 'create_task.html', {
            'form': TasksForm
        })
    else:
        try:
            form = TasksForm(request.POST)
            new_tasks = form.save(commit=False)
            new_tasks.user = request.user
            new_tasks.save()
            return redirect(tasks)
        except ValueError:
            return render(request, 'create_task.html', {
                    'form': TasksForm,
                    'error': 'Please provide valide data'
                })
        
        

def signout(request):
    logout(request)
    return redirect(home)

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(request, username=request.POST['username'], 
            password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': 'Username or Password is incorrect'
            })
        else:
            login(request, user)
            return redirect(tasks)


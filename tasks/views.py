from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    return HttpResponse("Welcome to task management system")

def contact(request):
    return HttpResponse("<h1 style='color:red'>This is contact</h1>")

def show_tasks(request):
    return HttpResponse("<h1 style='color:green'>This is show tasks</h1>")
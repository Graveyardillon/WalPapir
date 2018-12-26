from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'walpapir/home1.html')

def withChara(request):
    return render(request, 'walpapir/withChara.html')

def noChara(request):
    return render(request, 'walpapir/noChara.html')

def how2use(request):
    return render(request, 'walpapir/how2use.html')

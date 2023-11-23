from django.shortcuts import render

def index(request):
    return render(request, 'home.html')

def statistic(request):
    return render(request, 'statistic.html')

def about_us(request):
    return render(request, 'about_us.html')
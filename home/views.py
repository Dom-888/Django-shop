from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'home/index.html') # Return the index page
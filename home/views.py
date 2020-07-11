from django.shortcuts import render

# Questa è la base da cui partire per creare le views delle varie apps, passando nel secondo argomento my_app/my_app.html

def index(request):
    return render(request, 'home/index.html') # Return the index page


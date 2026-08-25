from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import get_template
from django.template import Template, Context



def home(request):
    #ruta de la plantilla
    # plantilla = open("benignoweb\home.html")
    # template = Template(plantilla.read())
    # plantilla.close()
    # contexto = Context()
    # document = template.render(contexto)
    plantilla = get_template('home.html')
    return render(request, 'home.html')

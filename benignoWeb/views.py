from django.http import HttpResponse
from django.template import Template, Context

def home(request):
    #ruta de la plantilla
    plantilla = open("benignoweb\plantilla\home.html")
    template = Template(plantilla.read())
    plantilla.close()
    contexto = Context()
    document = template.render(contexto)
    return HttpResponse(document)
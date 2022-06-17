
from email.policy import default
from django.http import HttpResponseRedirect

from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework import status 

#from django.urls import reverse

from django.shortcuts import render
from django import forms
import time

# Create your views here.
from app.boiler.serializers import CurrentProgramSerializer
from app.boiler.models import *

days_choices = ( 
    (1,"Lunes"),
    (2,"Martes"),
    (3,"Miercoles"),
    (4,"Jueves"),
    (5,"Viernes"),
    (6,"Sábado"),
    (7,"Domingo"),
    )

duration_choices = (
    (15,"15 mins"),
    (30,"30 mins"),
    (45,"45 mins"),
    (60,"60mins"),
    (90,"90 mins"),
    (120,"120 mins"),
)



'''
Pagina principal
'''

# regresa el json del programa actual si el bolier está encendido
def getBolierStatus():
    estado = CurrentProgram.objects.all().first()
    if estado:
        return estado
    return False
class BoilerOnForm(forms.Form):
    duration = forms.ChoiceField(label="duración",choices=duration_choices)


def index(request):
    if request.method == "POST":
        p = request.POST
        if request.POST.__contains__("borrar"):
            if request.POST.getlist("todos"):
                programs = Programs.objects.all()
                programs.delete()
                print("Borrar todos")
            elif request.POST.getlist("programs"):
                programs_keys = request.POST.getlist('programs')
                for program_key in programs_keys:
                    program = Programs.objects.get(pk=program_key)
                    program.delete()
                print(f"Borara algunos {p}")
            else:
                print("Nada seleccionado")
        else:
            form = BoilerOnForm(request.POST)
            if form.is_valid():
                if request.POST['onoff'] == "Apagar":
                    records = CurrentProgram.objects.all()
                    records.delete()
                elif request.POST['onoff'] == "Encender":
                    duration = request.POST['duration']
                    if duration:
                        actual = CurrentProgram.objects.all()
                        actual.delete()
                        t = time.localtime()
                        day = t.tm_wday+1            
                        hour = t.tm_hour
                        minutes = t.tm_min
                        data = {
                            "duration" : duration,
                            "day":day,                 
                            "hour": hour,
                            "minutes": minutes,
                            }
                        serializer = CurrentProgramSerializer(data=data)
                        if serializer.is_valid():
                            serializer.save()
                            return HttpResponseRedirect(reverse("index"))
                        else:
                            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return HttpResponseRedirect(reverse("index"))

    if request.method == "GET":
        return render(request,"boiler/index.html",{
            "programs":Programs.objects.all(),
            "form" : BoilerOnForm(),
            "boilerOn":getBolierStatus()
        })

'''
Programar un evento
'''
class newProgramForm(forms.Form):
    day = forms.ChoiceField(label="dia",choices=days_choices)
    hour = forms.IntegerField(label="hora",min_value=1,max_value=24)
    minutes = forms.IntegerField(label="minutos",min_value=0,max_value=59)
    duration = forms.ChoiceField(label="duración",choices=duration_choices)
    #active = forms.BooleanField(label="activo",required=False)



def addProgram(request):
    if request.method == "POST":
        form = newProgramForm(request.POST)
        if form.is_valid():
            day = form.cleaned_data['day']
            hour = form.cleaned_data['hour']
            minutes = form.cleaned_data['minutes']
            duration = form.cleaned_data['duration']
            Programs.objects.create(
                day = day,
                hour = hour,
                minutes = minutes,
                duration = duration,
                active = True,
            )
            return HttpResponseRedirect(reverse("index"))
    t = time.localtime()
    return render(request, "boiler/new_program.html", {
         "form" : newProgramForm(initial={'day':t.tm_wday+1})
    })   





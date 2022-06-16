
from django.http import HttpResponseRedirect, JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status 
from app.boiler.serializers import ProgramSerializer, CurrentProgramSerializer

from rest_framework.reverse import reverse
#from django.urls import reverse

from django.shortcuts import render
from django import forms
import requests
import time
import socket

# Create your views here.



days_choices = ( 
    (0,"Hoy"),
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

class BoilerOnForm(forms.Form):
    duration = forms.ChoiceField(label="duración",choices=duration_choices)

def index(request):
    if request.method == "POST":
        form = BoilerOnForm(request.POST)
        if form.is_valid():
            if request.POST['onoff'] == "Apagar":
                pass
            elif request.POST['onoff'] == "Encender":
                pass
            return HttpResponseRedirect(reverse("index"))
    if request.method == "GET":
        return render(request,"boiler/index.html",{
            "programs":Programs.objects.all(),
            "form" : BoilerOnForm(),
            "boilerOn":boilerOn(request)
        })

'''
Programar un evento
'''
class newProgramForm(forms.Form):
    day = forms.ChoiceField(label="dia",choices=days_choices)
    hour = forms.IntegerField(label="hora",min_value=1,max_value=24)
    minutes = forms.IntegerField(label="minutos",min_value=0,max_value=59)
    duration = forms.ChoiceField(label="duración",choices=duration_choices)
    active = forms.BooleanField(label="activo",required=False)



def addProgram(request):
    if request.method == "POST":
        form = newProgramForm(request.POST)
        if form.is_valid():
            day = form.cleaned_data['day']
            hour = form.cleaned_data['hour']
            minutes = form.cleaned_data['minutes']
            duration = form.cleaned_data['duration']
            active = form.cleaned_data['active']
            unic= day == '0'
            if unic:
                day = time.localtime().tm_wday+1
            Programs.objects.create(
                day = day,
                hour = hour,
                minutes = minutes,
                duration = duration,
                active = active,
                unic=unic
            )
            return HttpResponseRedirect(reverse("index"))
    return render(request, "boiler/new_program.html", {
        "form" : newProgramForm()
    })

def boilerOn(request):
    # determina la url completa (eso evitó que tuviera que alambrar aqui 127.0.0.1 o cualquier otra url)
    # tuve que pasar como parámetro el objeto request... eso no me gustó
    # espero que haya algubna forma de corregir
    # Ojo tuve que usar:
    #    from rest_framework.reverse import reverse
    # en lugar de la clasica
    #    from django.urls import reverse    
    url = reverse('boilerStatus',request=request)
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return False

def boilerOff(request):
    # determina la url completa (eso evitó que tuviera que alambrar aqui 127.0.0.1 o cualquier otra url)
    # tuve que pasar como parámetro el objeto request... eso no me gustó
    # espero que haya algubna forma de corregir
    # Ojo tuve que usar:
    #    from rest_framework.reverse import reverse
    # en lugar de la clasica
    #    from django.urls import reverse    
    url = reverse('boilerStatus',request=request)
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return False





# ------- views for Json and djangoREST ---------------------
def ping(request):
    data = {"ping":"pong!"}
    return JsonResponse(data)

class PostPing(APIView):
    def post(self,request):
        if len(request.data)==1 and 'name' in request.data:
            data = { "ping" : "pong "+request.POST['name']}
        return JsonResponse(data)


class ProgramsList(APIView):
    def get(self, request):
        programs = Programs.objects.order_by("day","hour","minutes","active")
        serializer = ProgramSerializer(programs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ProgramSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return  Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        if len(request.data)==1 and 'key' in request.data:
            key = request.POST['key']
            records = CurrentProgram.objects.find(key=key)
            if len(records)==1:
                records.delete()
                return  Response(status=status.HTTP_200_OK) 
            return Response(status=status.HTTP_400_BAD_REQUEST)    
        return Response(status=status.HTTP_400_BAD_REQUEST)    

class ProgramDetails(APIView):
    def get(self, request, pk):
        program = Programs.objects.filter(pk=pk).first()
        if program:
            serializer = ProgramSerializer(program)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status = status.HTTP_404_NOT_FOUND)

class CurrentProgramList(APIView):
    def get(self, request):
        programs = CurrentProgram.objects.all()
        serializer = CurrentProgramSerializer(programs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        if len(request.data)==1 and 'duration' in request.data:
            # si solo se envio un valor y ese valor es duration 
            duration = request.POST['duration']
            if duration:
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
                    return  Response(serializer.data, status=status.HTTP_201_CREATED) 
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)    
        return Response(status=status.HTTP_400_BAD_REQUEST)   


    def delete(self, request):
        if len(request.data)==1 and 'confirm' in request.data:
            confirm = request.POST['confirm']
            if confirm == "yes":
                records = CurrentProgram.objects.all()
                records.delete()
                return  Response(status=status.HTTP_200_OK) 
            return Response(status=status.HTTP_400_BAD_REQUEST)    
        return Response(status=status.HTTP_400_BAD_REQUEST)    

        
        return Response(status = status.HTTP_404_NOT_FOUND)           




    

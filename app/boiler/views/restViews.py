
from django.http import HttpResponseRedirect, JsonResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status 


from app.boiler.serializers import ProgramSerializer, CurrentProgramSerializer
from app.boiler.models import CurrentProgram, Programs


import time

# Create your views here.


# ------- views for Json and djangoREST ---------------------

    


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
                current = CurrentProgram.objects.all()
                current.delete()
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




    
def ping(request):
    data = {"ping":"pong!"}
    return JsonResponse(data)

class PostPing(APIView):
    def post(self,request):
        if len(request.data)==1 and 'name' in request.data:
            data = { "ping" : "pong "+request.POST['name']}
        return JsonResponse(data)


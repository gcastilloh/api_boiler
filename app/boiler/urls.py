from django.urls import path
from app.boiler.views import ping, ProgramsList, ProgramDetails, CurrentProgramList
from  app.boiler.views import addProgram
from app.boiler.views import ping, PostPing, index

urlpatterns = [
    path("indexing",index,name="index"),
    path("ping/", ping, name="ping"),
    path("postPing/", PostPing.as_view(), name="postPing"),
    path("programs",ProgramsList.as_view(), name="programs"),
    path("programs/<int:pk>",ProgramDetails.as_view(),name="programs_pk"),  
    path("current",CurrentProgramList.as_view(), name="current"),

#    path("boilerStatus",BoilerStatus.as_view(), name="boilerStatus"),  
#    path("boilerOn",BoilerOn.as_view(), name="boilerOn"),  
    path("nuevo",addProgram, name="addProgram"),


]
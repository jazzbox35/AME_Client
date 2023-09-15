from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("CreateNewCase", views.CreateNewCase, name="CreateNewCase"), 
    path("TrainCase", views.TrainCase, name="TrainCase"), 
    path("AddProposition", views.AddProposition, name="AddProposition"), 
]

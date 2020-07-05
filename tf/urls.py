from django.contrib import admin
from django.urls import path
from . import views

app_name = 'tf'

urlpatterns = [
    path('', views.index, name="index"),
    path('uploadvideo/', views.uploadvideo.as_view(), name="uploadvideo"),
    path('afterupload/', views.afterupload, name="afterupload"),
    path('tensorflow/', views.tensorflow, name="tensorflow"),
    path('frames/', views.frames, name="frames"),
    path('videoresult/', views.videoresult, name="videoresult"),
    path('frames/<int:id>', views.frames, name="frames"),
    path('videoresult/<int:id>', views.videoresult, name="videoresult"),
]

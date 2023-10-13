from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_video, name='upload_video'),
    path('transcription/<int:id>/', views.view_transcription, name='view_transcription'),
]

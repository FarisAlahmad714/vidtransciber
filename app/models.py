from django.db import models
from django import forms

class Transcription(models.Model):
    video = models.FileField(upload_to='videos/')
    text = models.TextField(blank=True)

class VideoForm(forms.ModelForm):
    class Meta:
        model = Transcription  # Replace with your actual model
        fields = ['video']
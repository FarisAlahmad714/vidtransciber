from django.shortcuts import render, redirect
from django.conf import settings
from .models import Transcription ,VideoForm
from moviepy.editor import *
import speech_recognition as sr
from django.http import HttpResponse
import logging


logging.basicConfig(filename='transcribe.log', level=logging.DEBUG)

def home(request):
    return HttpResponse("Welcome to the homepage!")

def transcribe_audio(audio_path):
    r = sr.Recognizer()
    try:
        with sr.AudioFile(audio_path) as source:
            audio_data = r.record(source)
            text = r.recognize_google(audio_data, key=settings.GOOGLE_API_KEY)
        return text
    except sr.UnknownValueError:
        logging.error("Google Web Speech API could not understand the audio.")
    except sr.RequestError as e:
        logging.error(f"Could not request results from Google Web Speech API; {e}")
    return ""

    


def convert_video_to_audio(video_path):
    audio_path = video_path.replace(".mp4", ".wav")
    audioclip = AudioFileClip(video_path)
    audioclip.write_audiofile(audio_path)
    return audio_path

def upload_video(request):
    context = {}
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save()
            audio_path = convert_video_to_audio(instance.video.path)
        else:
            logging.error(form.errors)
            try:
                text = transcribe_audio(audio_path)
                # Save transcribed text to database associated with video
                instance.transcription = text
                instance.save()
            except Exception as e:
                # Handle the exception and maybe log it for debugging
                text = "Error transcribing the audio."

            # Render video and transcription in template
            context = {
                'video': instance,
                'transcription': text
            }



    return render(request, 'upload.html', context)

def view_transcription(request, id):
    transcription = Transcription.objects.get(id=id)
    return render(request, 'transcription.html', {'transcription': transcription})

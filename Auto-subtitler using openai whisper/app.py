import moviepy.editor
from datetime import timedelta
import os
import whisper
import google.generativeai as genai
import gradio as gr

# step1: extracting audio from video
video=moviepy.editor.VideoFileClip('tamil.mp4')
audio=video.audio
audio.write_audiofile('1.mp3')


# using opemai whisper to generate text from audio in almost 50 languages including 
model = whisper.load_model("base")
print("Whisper model loaded.")

# defining a transcribe function
def transcribe_audio(path):
    transcribe = model.transcribe(audio=path)
    segments = transcribe['segments']

    for segment in segments:
        startTime = str(0)+str(timedelta(seconds=int(segment['start'])))+',000'
        endTime = str(0)+str(timedelta(seconds=int(segment['end'])))+',000'
        text = segment['text']
        segmentId = segment['id']+1 
        segment = f"{segmentId}\n{startTime} --> {endTime}\n{text[1:] if text[0] is ' ' else text}\n\n"
        srtFilename = os.path.join("inTamil.srt")
        with open(srtFilename, 'a', encoding='utf-8') as srtFile:
            srtFile.write(segment)
    return srtFilename


# one examplevvv
transcribe_audio("tamil.mp4")
import os
import subprocess
import gradio as gr
from base64 import b64encode
from whisper import load_model
from whisper.utils import write_srt

# Load the Whisper model
model = load_model("medium")

def video_to_mp3(video_file, output_ext="mp3"):
    """Converts a video file to MP3 format."""
    filename, ext = os.path.splitext(video_file)
    subprocess.call(["ffmpeg", "-y", "-i", video_file, f"{filename}.{output_ext}"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.STDOUT)
    return f"{filename}.{output_ext}"

def generate_srt(video_file, text_file):
    """Generates SRT subtitle file by transcribing the audio from the video."""
    # Convert video to MP3
    audio_file = video_to_mp3(video_file)

    # Transcribe audio using Whisper model
    result = model.transcribe(audio_file)

    # Write SRT file
    with open(text_file, "r", encoding="utf-8") as f:
        script = f.read()

    output_srt = video_file.split(".")[0] + ".srt"
    write_srt(script, result["segments"], output_srt)

    return output_srt

def launch_gradio():
    """Launches the Gradio interface."""
    block = gr.Blocks()

    with block:
        with gr.Group():
            with gr.Box():
                with gr.Row().style():
                    input_video = gr.Video(
                        label="Input Video",
                        type="filepath",
                        mirror_webcam=False
                    )
                    input_text = gr.Textbox(
                        label="Input Text File",
                        type="file",
                        accept=".txt"
                    )
                    output_srt = gr.Output()
                btn = gr.Button("Generate SRT")

        btn.click(generate_srt, inputs=[input_video, input_text], outputs=[output_srt])

        gr.HTML('''
        <div class="footer">
                    <p>Model by <a href="https://github.com/openai/whisper" style="text-decoration: underline;" target="_blank">OpenAI</a> - Gradio App by <a href="https://twitter.com/1littlecoder" style="text-decoration: underline;" target="_blank">1littlecoder</a>
                    </p>
        </div>
        ''')

    block.launch(debug=True)

if _name_ == "_main_":
    launch_gradio()
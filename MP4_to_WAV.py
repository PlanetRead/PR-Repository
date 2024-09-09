def mp4_to_wav(mp4, wav):
    video = VideoFileClip(mp4)
    video.audio.write_audiofile(wav, codec='pcm_s16le')

# Example usage:
mp4_file_path = 'input.mp4'
wav_file_path = 'output.wav'
mp4_to_wav(mp4_file_path, wav_file_path)